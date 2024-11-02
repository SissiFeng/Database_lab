{{
    config(
        materialized='incremental',
        unique_key='experiment_sk',
        tags=['performance']
    )
}}

with experiment_metrics as (
    select * from {{ ref('int_experiment_metrics') }}
),

analysis_results as (
    select * from {{ ref('stg_analysis_results') }}
),

final as (
    select
        em.experiment_sk,
        em.experiment_id,
        em.protocol_version,
        em.total_samples,
        em.completed_samples,
        em.avg_sample_processing_time,
        count(distinct ar.analysis_id) as total_analyses,
        avg(ar.confidence_score) as avg_confidence_score,
        sum(case when ar.validation_status = 'valid' then 1 else 0 end) as valid_results_count
    from experiment_metrics em
    left join analysis_results ar on em.experiment_id = ar.experiment_id
    group by 1, 2, 3, 4, 5, 6
)

select 
    *,
    {{ get_audit_columns() }}
from final

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
