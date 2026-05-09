from services import (
    listar_modelos, cadastrar_veiculo_por_modelo, comparar_co2,
    registrar_uso_taggy, obter_painel_impacto, listar_recompensas_catalogo
)

def menu():
    while True:
        print("\n==== ECOMETRIC ====")
        print("1 - Listar Modelos")
        print("2 - Cadastrar Veículo")
        print("3 - Simular Economia de CO2")
        print("4 - Registrar Uso da Taggy (Ganhar Pontos)")
        print("5 - Meu Painel de Impacto Ambiental")
        print("6 - Ver Catálogo de Recompensas (Loja)")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            for m in listar_modelos(): print(f"{m[0]} - {m[1]} ({m[2]})")

        elif op == "2":
            placa = input("Placa: ")
            mod_id = int(input("ID Modelo: "))
            cadastrar_veiculo_por_modelo(placa, mod_id)
            print("✅ Veículo cadastrado!")

        elif op == "3":
            placa = input("Placa: ")
            tipo = input("Tipo (shopping/pedagio): ")
            try:
                s, c, eco, t = comparar_co2(placa, tipo)
                print(f"Economia estimada: {eco:.2f}g de CO2")
            except Exception as e: print(e)

        elif op == "4":
            placa = input("Placa: ")
            tipo = input("Tipo: ")
            try:
                p, b, q = registrar_uso_taggy(placa, tipo)
                print(f"🎉 +{p} CapCoins acumulados! (Total no mês: {q})")
                if b > 0: print(f"🔥 BÔNUS DE FREQUÊNCIA: +{b} CapCoins!")
            except Exception as e: print(e)

        elif op == "5":
            placa = input("Placa: ")
            saldo, total, co2, folhas = obter_painel_impacto(placa)
            print(f"\n📊 PAINEL DO USUÁRIO [{placa}]")
            print(f"💰 Saldo: {saldo} CapCoins")
            print(f"🌱 CO2 Evitado: {co2}g")
            print(f"📄 Folhas de papel poupadas: {folhas}")
            if saldo >= 100: print("🎁 Você já pode resgatar um prêmio na opção 6!")

        elif op == "6":
            print("\n🎁 CATÁLOGO DE RECOMPENSAS")
            for r in listar_recompensas_catalogo():
                print(f"• {r[0]} | Custo: {r[1]} CapCoins")

        elif op == "0": break

if __name__ == "__main__":
    menu()