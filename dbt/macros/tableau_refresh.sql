{% macro generate_tableau_refresh_script() %}
    {% set exposures = graph.exposures.values() %}
    
    {% if exposures | length > 0 %}
        {% for exposure in exposures %}
            {% if exposure.meta.tableau is defined %}
                -- Generate Tableau REST API refresh commands
                select
                    '{{ exposure.name }}' as exposure_name,
                    '{{ exposure.meta.tableau.workbook_name }}' as workbook_name,
                    '{{ exposure.meta.tableau.project }}' as project,
                    '{{ exposure.meta.tableau.refresh_schedule }}' as refresh_schedule,
                    array[
                        {% for dep in exposure.depends_on %}
                            '{{ dep }}'
                            {% if not loop.last %},{% endif %}
                        {% endfor %}
                    ] as dependencies,
                    '{{ exposure.url }}' as dashboard_url,
                    '{{ exposure.owner.name }}' as owner_name,
                    '{{ exposure.owner.email }}' as owner_email
                {% if not loop.last %}
                union all
                {% endif %}
            {% endif %}
        {% endfor %}
    {% endif %}
{% endmacro %}
