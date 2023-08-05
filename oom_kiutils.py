import oom_base

def symbol_change_name_oomp(**kwargs):
    library_name = kwargs['library_name']    
    repo = kwargs['repo']
    owner = repo['owner']    
    symbol = kwargs['symbol']
    try:
        entry_name = oom_base.remove_special_characters(symbol.entryName)
        entry_name_original = symbol.entryName
    except:
        entry_name = oom_base.remove_special_characters(symbol.id)
        entry_name_original = symbol.id

                   
    entry_name = oom_base.remove_special_characters(f'{owner}_{library_name}_{entry_name}')
    entry_name = entry_name.lower()                    
    
    try:
        extra_entry_name = symbol.entryName.replace(entry_name_original, entry_name)
        extra_entry_name = oom_base.remove_special_characters(extra_entry_name)
        symbol.entryName = symbol.entryName.replace(entry_name_original, extra_entry_name)
    except:
        extra_entry_name = symbol.entryName.replace(entry_name_original, entry_name)
        extra_entry_name = oom_base.remove_special_characters(extra_entry_name)
        symbol.id = symbol.id.replace(entry_name_original, extra_entry_name)
    for unit in symbol.units:
        try:
            test = unit.entryName
            extra_entry_name = unit.entryName.replace(entry_name_original, entry_name)
            extra_entry_name = oom_base.remove_special_characters(extra_entry_name)
            unit.entryName = extra_entry_name
        except:
            extra_entry_name = unit.id.replace(entry_name_original, entry_name)
            extra_entry_name = oom_base.remove_special_characters(extra_entry_name)
            unit.id = unit.id.replace(entry_name_original, entry_name)
    #if extends
    if "10m03" in entry_name:
        pass
    if symbol.extends != None:
        extend_extra = f'{owner}_{library_name}'
        extend_extra = oom_base.remove_special_characters(f'{extend_extra}_{symbol.extends}')
        symbol.extends = extend_extra

    return symbol
    

def get_oomp_deets_symbol(**kwargs):
    symb = kwargs.get('symb', None)
    repo = symb['repo']
    owner = repo['owner']
    symbol = symb['symbol']
