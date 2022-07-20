{% obj.c_struct %}

{% if obj.is_variable_size %}
    {obj.c_struct_head} // c_struct_head is first fixed sizes
{% endif %}
