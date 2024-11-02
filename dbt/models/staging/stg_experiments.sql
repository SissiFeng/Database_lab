with source as (
    select * from {{ source('raw', 'experiments') }}
),

renamed as (
    select
        {{ generate_surrogate_key(['experiment_id', 'start_time']) }} as experiment_sk,
        experiment_id,
        protocol_version,
        configuration,
        status,
        planned_start_time,
        actual_start_time,
        actual_end_time,
        created_at,
        updated_at
    from source
),

final as (
    select
        *,
        case 
            when status = 'completed' 
            then datediff('minute', actual_start_time, actual_end_time)
        end as duration_minutes
    from renamed
    where not is_deleted
)

select * from final
