import dagster as dg
import pandas as pd

# Mapping from ANZSCO2 occupation group titles (as they appear in the IVI data)
# to UAC Field of Study categories. This is the join key for opportunity gap
# analysis: comparing job market demand with student preference share.
_MAPPING = [
    ("Medical Practitioners and Nurses", "Health"),
    ("Health Diagnostic and Therapy Professionals", "Health"),
    ("ICT Professionals", "Information Technology"),
    ("Engineers", "Engineering & Related Technologies"),
    ("Education Professionals", "Education"),
    ("Legal, Social and Welfare Professionals", "Society & Culture"),
    ("Business, Finance and Human Resource Professionals", "Management & Commerce"),
    ("Sales, Marketing & Public Relations Professionals", "Management & Commerce"),
    ("Arts and Media Professionals", "Creative Arts"),
    ("Science Professionals and Veterinarians", "Natural & Physical Sciences"),
    ("Transport and Design Professionals, and Architects", "Architecture & Building"),
    ("Health and Welfare Support Workers", "Health"),
]


@dg.asset(
    group_name="reference_data",
    tags={"source": "manual", "domain": "mapping", "update_frequency": "static"},
)
def occupation_fos_mapping(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """ANZSCO2 occupation group to UAC Field of Study mapping.

    Source: Manual curation, no download required
    Marketing use: Join key for opportunity gap analysis — links job vacancy
        demand (from IVI) to student preference share (from UAC FOS data).
        Occupations with high vacancy growth but low student preference
        represent messaging opportunities.
    Format: anzsco2_title, uac_field_of_study
    Limitations:
    - Not all ANZSCO2 groups map cleanly to a single UAC field
    - Some UAC fields (e.g. Mixed Field Programs, Food/Hospitality) have
      no clear ANZSCO2 professional-level match
    - Mapping is approximate and manually maintained
    """
    df = pd.DataFrame(_MAPPING, columns=["anzsco2_title", "uac_field_of_study"])

    context.log.info(f"Loaded {len(df)} occupation-to-FOS mappings")

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "unique_occupations": dg.MetadataValue.int(df["anzsco2_title"].nunique()),
        "unique_fields_of_study": dg.MetadataValue.int(
            df["uac_field_of_study"].nunique()
        ),
    })

    return df
