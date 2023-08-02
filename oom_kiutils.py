

def symbol_change_name_oomp(**kwargs):
    library_name = kwargs['library_name']    
    repo = kwargs['repo']
    owner = repo['owner']
    entry_name = kwargs['entry_name']
    symbol = kwargs['symbol']


    entry_name = f'{owner}_{library_name}_{symbol.entryName}'                    
    entry_name_original = symbol.entryName
    symbol.entryName = symbol.entryName.replace(entry_name_original, entry_name)
    for unit in symbol.units:
        unit.entryName = unit.entryName.replace(entry_name_original, entry_name)
    #if extends
    if symbol.extends != None:
        extend_extra = f'{owner}_{library_name}'
        symbol.extends = f'{extend_extra}_{symbol.extends}'

    return symbol
    

def get_oomp_deets_symbol(**kwargs):
    symb = kwargs.get('symb', None)
    repo = symb['repo']
    owner = repo['owner']
    symbol = symb['symbol']
