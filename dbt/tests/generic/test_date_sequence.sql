{% test date_sequence(model, column_name, date_part='day') %}

with validation as (
    select
        {{ column_name }} as date_value,
        lead({{ column_name }}) over (order by {{ column_name }}) as next_date_value
    from {{ model }}
),

validation_errors as (
    select *
    from validation
    where datediff('{{ date_part }}', date_value, next_date_value) > 1
)

select count(*)
from validation_errors

{% endtest %}
