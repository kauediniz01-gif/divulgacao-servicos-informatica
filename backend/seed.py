
from database import conectar


def cadastrar_dados():
    categorias = [
        ("Montagem de computadores", "Montagem e instalação de componentes."),
        ("Manutenção e limpeza", "Limpeza, manutenção preventiva e diagnóstico."),
        ("Upgrade de hardware", "Atualização e melhoria de componentes."),
        ("Software e sistemas", "Instalação e configuração de sistemas e programas.")
    ]

    servicos = [
        
        ("Montagem de PC", "Montagem completa de computadores a partir dos componentes escolhidos.", "Montagem de computadores"),
        ("Instalação de componentes", "Instalação de peças e componentes compatíveis com o computador.", "Montagem de computadores"),
        ("Organização de cabos", "Organização interna dos cabos para melhorar a montagem e a circulação de ar.", "Montagem de computadores"),
        ("Instalação de fonte de alimentação", "Instalação e conexão da fonte de alimentação do computador.", "Montagem de computadores"),


        ("Limpeza interna", "Remoção de poeira e sujeira dos componentes.", "Manutenção e limpeza"),
        ("Troca de pasta térmica", "Substituição da pasta térmica do processador.", "Manutenção e limpeza"),
        ("Manutenção preventiva", "Cuidados para preservar o funcionamento do computador.", "Manutenção e limpeza"),
        ("Diagnóstico de problemas", "Identificação de possíveis falhas no computador.", "Manutenção e limpeza"),

        ("Instalação de memória RAM", "Instalação ou substituição de memória RAM.", "Upgrade de hardware"),
        ("Instalação de SSD", "Instalação de unidade SSD para armazenamento.", "Upgrade de hardware"),
        ("Troca de placa de vídeo", "Substituição ou instalação de placa de vídeo.", "Upgrade de hardware"),
        ("Atualização de processador", "Substituição do processador por outro compatível.", "Upgrade de hardware"),

        ("Instalação do Windows", "Instalação e configuração do sistema operacional Windows.", "Software e sistemas"),
        ("Instalação de drivers", "Instalação dos drivers necessários para o funcionamento do computador.", "Software e sistemas"),
        ("Instalação de programas", "Instalação e configuração de programas.", "Software e sistemas"),
        ("Instalação de fans (ventoinhas)", "Instalação e conexão de ventoinhas para refrigeração do gabinete.", "Upgrade de hardware"),
        ("Instalação de water cooler", "Instalação e conexão de sistema de refrigeração líquida.", "Upgrade de hardware"),
        ("Troca de gabinete", "Substituição do gabinete e organização dos componentes.", "Upgrade de hardware"),
        ("Troca de placa-mãe", "Substituição da placa-mãe por um modelo compatível.", "Upgrade de hardware"),
    ]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO categorias (nome, descricao)
        VALUES (?, ?)
    """, categorias)

    for nome, descricao, categoria in servicos:
        cursor.execute("""
            SELECT id_categoria FROM categorias WHERE nome = ?
        """, (categoria,))

        resultado = cursor.fetchone()

        cursor.execute("""
            INSERT INTO servicos (nome, descricao, categoria_id)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM servicos
                WHERE nome = ? AND categoria_id = ?
            )
        """, (nome, descricao, resultado["id_categoria"], nome, resultado["id_categoria"]))

    conexao.commit()
    conexao.close()

    print("Categorias e serviços cadastrados com sucesso!")


if __name__ == "__main__":
    cadastrar_dados()
