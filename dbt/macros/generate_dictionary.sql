{% macro generate_data_dictionary() %}
    {% set models_in_exposures = [] %}
    
    {% for exposure in graph.exposures.values() %}
        {% for dependency in exposure.depends_on %}
            {% if dependency.startswith('ref(') %}
                {% do models_in_exposures.append(dependency.replace("ref('", "").replace("')", "")) %}
            {% endif %}
        {% endfor %}
    {% endfor %}
    
    {% for model in graph.nodes.values() %}
        {% if model.resource_type == 'model' and model.name in models_in_exposures %}
            select
                '{{ model.name }}' as model_name,
                '{{ model.description }}' as model_description,
                array[
                    {% for exposure in graph.exposures.values() %}
                        {% if model.unique_id in exposure.depends_on %}
                            '{
                                "name": "{{ exposure.name }}",
                                "type": "{{ exposure.type }}",
                                "url": "{{ exposure.url }}"
                            }'
                        {% endif %}
                    {% endfor %}
                ] as used_in_exposures,
                {{ generate_column_docs(model.columns) }} as columns
            {% if not loop.last %}
            union all
            {% endif %}
        {% endif %}
    {% endfor %}
{% endmacro %}
