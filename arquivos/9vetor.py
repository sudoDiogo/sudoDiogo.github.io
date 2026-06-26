tabela_atual = ['10.0.0.0/8', '172.16.0.0/12', '192.168.1.0/24','203.0.113.0/24', '198.51.100.0/24']
rota_removida = '203.0.113.0/24'
rotas_inseridas = ['10.10.0.0/16' ,  '192.168.100.0/24']

tabela_antiga = tabela_atual.copy()
tabela_nova = tabela_atual.copy()

if rota_removida in tabela_nova:
    tabela_nova.remove(rota_removida)

tabela_nova.extend(rotas_inseridas)

rotas_adicionadas = list(set(tabela_nova) - set(tabela_antiga))
rotas_removidas = list(set(tabela_antiga) - set(tabela_nova))

print(f"Inseridas: {rotas_adicionadas} ")
print(f"Removidas: {rotas_removidas} ")