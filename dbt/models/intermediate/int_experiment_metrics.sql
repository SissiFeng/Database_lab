with experiments as (
    select * from {{ ref('stg_experiments') }}
),

samples as (
    select * from {{ ref('stg_samples') }}
),

metrics as (
    select
        e.experiment_sk,
        e.experiment_id,
        e.protocol_version,
        count(distinct s.sample_id) as total_samples,
        sum(case when s.status = 'completed' then 1 else 0 end) as completed_samples,
        avg(s.processing_time) as avg_sample_processing_time,
        min(s.processing_time) as min_sample_processing_time,
        max(s.processing_time) as max_sample_processing_time
    from experiments e
    left join samples s on e.experiment_id = s.experiment_id
    group by 1, 2, 3
)

select * from metrics
