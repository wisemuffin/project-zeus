import dagster as dg
import pandas as pd

# Mapping from SOC 2020 major groups to CAH (Common Aggregation Hierarchy)
# Level 1 subject areas. This is the join key for opportunity gap analysis:
# comparing labour market demand (from ONS vacancy data) with student
# preference share (from UCAS admissions data).
#
# SOC 2020 major groups (9 groups, 1-digit codes):
#   1 - Managers, directors and senior officials
#   2 - Professional occupations
#   3 - Associate professional and technical occupations
#   4 - Administrative and secretarial occupations
#   5 - Skilled trades occupations
#   6 - Caring, leisure and other service occupations
#   7 - Sales and customer service occupations
#   8 - Process, plant and machine operatives
#   9 - Elementary occupations
#
# CAH Level 1 has 23 subject groups. Not all CAH subjects map to a
# professional-level SOC group; some (e.g. Combined & general studies,
# Humanities & liberal arts) have diffuse employment outcomes.

_MAPPING = [
    # SOC 1 — Managers, directors and senior officials
    ("1", "Managers, directors and senior officials", "Business & management"),

    # SOC 2 — Professional occupations (broad: health, education, science, tech, legal, business)
    ("2", "Professional occupations", "Medicine & dentistry"),
    ("2", "Professional occupations", "Subjects allied to medicine"),
    ("2", "Professional occupations", "Engineering & technology"),
    ("2", "Professional occupations", "Computing"),
    ("2", "Professional occupations", "Education & teaching"),
    ("2", "Professional occupations", "Law"),
    ("2", "Professional occupations", "Physical sciences"),
    ("2", "Professional occupations", "Mathematical sciences"),
    ("2", "Professional occupations", "Veterinary sciences"),
    ("2", "Professional occupations", "Architecture, building & planning"),

    # SOC 3 — Associate professional and technical occupations
    ("3", "Associate professional and technical occupations", "Subjects allied to medicine"),
    ("3", "Associate professional and technical occupations", "Business & management"),
    ("3", "Associate professional and technical occupations", "Creative arts & design"),
    ("3", "Associate professional and technical occupations", "Communications & media"),
    ("3", "Associate professional and technical occupations", "Computing"),

    # SOC 4 — Administrative and secretarial occupations
    ("4", "Administrative and secretarial occupations", "Business & management"),

    # SOC 5 — Skilled trades occupations
    ("5", "Skilled trades occupations", "Engineering & technology"),
    ("5", "Skilled trades occupations", "Architecture, building & planning"),
    ("5", "Skilled trades occupations", "Agriculture, food & related studies"),

    # SOC 6 — Caring, leisure and other service occupations
    ("6", "Caring, leisure and other service occupations", "Subjects allied to medicine"),
    ("6", "Caring, leisure and other service occupations", "Social sciences"),
    ("6", "Caring, leisure and other service occupations", "Education & teaching"),

    # SOC 7 — Sales and customer service occupations
    ("7", "Sales and customer service occupations", "Business & management"),

    # SOC 8 — Process, plant and machine operatives
    ("8", "Process, plant and machine operatives", "Engineering & technology"),

    # SOC 9 — Elementary occupations
    # No strong CAH mapping — these are typically non-graduate roles.
    # Omitted intentionally.
]


@dg.asset(
    group_name="reference_data",
    tags={
        "source": "manual",
        "domain": "mapping",
        "update_frequency": "static",
        "ingestion": "manual",
    },
    kinds={"python"},
)
def soc_cah_mapping(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """SOC 2020 major group to CAH Level 1 subject area mapping.

    What: Maps the 9 SOC 2020 major occupation groups (1-digit codes) to
        the 23 CAH (Common Aggregation Hierarchy) Level 1 subject areas used
        by HESA/UCAS. Many-to-many: one SOC group can link to multiple CAH
        subjects and vice versa.
    Use case: Join key for UK opportunity gap analysis — links labour demand
        (from ONS vacancy/employment data) to student preference share (from
        UCAS admissions data). Occupations with high demand but low student
        preference represent messaging opportunities for university marketing.
    Format: soc_major_group_code, soc_major_group_title, cah_level1_subject
    Limitations:
        - SOC major groups are very broad (9 groups); sub-major or minor
          groups would give more precise mappings but require more maintenance
        - SOC 9 (Elementary occupations) is omitted as these are typically
          non-graduate roles with no clear CAH subject link
        - Some CAH subjects (e.g. Combined & general studies, Humanities &
          liberal arts, Historical philosophical & religious studies) have no
          direct SOC major group match and are omitted
        - Mapping is approximate and manually maintained
    """
    df = pd.DataFrame(
        _MAPPING,
        columns=["soc_major_group_code", "soc_major_group_title", "cah_level1_subject"],
    )

    context.log.info(f"Loaded {len(df)} SOC-to-CAH mappings")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(df)),
            "unique_soc_groups": dg.MetadataValue.int(
                df["soc_major_group_code"].nunique()
            ),
            "unique_cah_subjects": dg.MetadataValue.int(
                df["cah_level1_subject"].nunique()
            ),
            "source_url": dg.MetadataValue.url(
                "https://www.ons.gov.uk/methodology/classificationsandstandards/standardoccupationalclassificationsoc/soc2020"
            ),
        }
    )

    return df
