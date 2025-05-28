"""Application utils"""
main_options = {
    'Produção': 'PRODUCAO',
    'Processamento': 'PROCESSAMENTO',
    'Comercialização': 'COMERCIALIZACAO',
    'Importação': 'IMPORTACAO',
    'Exportação': 'EXPORTACAO'
}

sub_options = {
    'Produção': 'Producao',
    'Viníferas': 'ProcessaViniferas',
    'Americanas e híbridas': 'ProcessaAmericanas',
    'Uvas de mesa': 'ProcessaMesa',
    'Sem classificação': 'ProcessaSemclass',
    'Comercialização': 'Comercio',
    'Vinhos de mesa (Imp)': 'ImpVinhos',
    'Espumantes (Imp)': 'ImpEspumantes',
    'Uvas frescas (Imp)': 'ImpFrescas',
    'Uvas passas (Imp)': 'ImpPassas',
    'Suco de uva (Imp)': 'ImpSuco',
    'Vinhos de mesa (Exp)': 'ExpVinho',
    'Espumantes (Exp)': 'ExpEspumantes',
    'Uvas frescas (Exp)': 'ExpUva',
    'Suco de uva (Exp)': 'ExpSuco'
}

columns = ['category_uid', 'subcategory', 'control', 'created_at', 'updated_at', 'year']
