"""Generic utilities, used by run.py and other scripts
"""

def get_configurations(configs):
    """Builds a list of all possible configuration dictionary
    from one configuration dictionary that contains all values for a key

    Args:
        configs (dict[str: List[any]]): a dictionary of configurations
    
    Returns:
        List: A list of configuration
    """
    if type(configs) == list:
        return configs
    all_configs = []
    config_keys = list(configs.keys())

    def recursive_config_list_builder(param_type_index, current_param_dict,
                                      param_list):
        if param_type_index == len(param_list):
            all_configs.append(current_param_dict)
        else:
            if type(configs[config_keys[param_type_index]]) == list:
                for val in configs[param_list[param_type_index]]:
                    temp = current_param_dict.copy()
                    temp[param_list[param_type_index]] = val
                    recursive_config_list_builder(param_type_index+1, temp,
                                                  param_list)
            else:
                temp = current_param_dict.copy()
                temp[param_list[param_type_index]] = configs[
                                            config_keys[param_type_index]]
                recursive_config_list_builder(param_type_index+1, temp,
                                              param_list)

    recursive_config_list_builder(0, dict(), config_keys)
    return all_configs