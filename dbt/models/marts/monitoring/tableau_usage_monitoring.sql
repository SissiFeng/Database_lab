{{
    config(
        materialized='incremental',
        unique_key=['workbook_name', 'date']
    )
}}

with tableau_logs as (
    select * from {{ source('tableau_logs', 'view_stats') }}
    {% if is_incremental() %}
    where log_date > (select max(date) from {{ this }})
    {% endif %}
),

exposure_mapping as (
    {{ generate_tableau_refresh_script() }}
),

usage_stats as (
    select
        em.exposure_name,
        em.workbook_name,
        tl.log_date as date,
        count(distinct tl.user_id) as unique_users,
        count(*) as total_views,
        avg(tl.duration_seconds) as avg_view_duration,
        max(tl.duration_seconds) as max_view_duration,
        array_agg(distinct tl.user_department) as user_departments
    from tableau_logs tl
    inner join exposure_mapping em 
        on tl.workbook_name = em.workbook_name
    group by 1, 2, 3
)

select
    us.*,
    em.dependencies,
    em.owner_name,
    em.owner_email,
    em.dashboard_url,
    current_timestamp as updated_at
from usage_stats us
left join exposure_mapping em 
    on us.exposure_name = em.exposure_name
