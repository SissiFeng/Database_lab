{% macro get_audit_columns() %}
    created_at timestamp default getdate(),
    created_by varchar(100) default current_user,
    updated_at timestamp default getdate(),
    updated_by varchar(100) default current_user,
    is_deleted boolean default false
{% endmacro %}

-- ... 其他宏定义 ...
