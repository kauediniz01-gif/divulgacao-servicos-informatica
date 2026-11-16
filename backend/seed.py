
from database import conectar


def cadastrar_dados():
    categorias = [
        ("Montagem de computadores", "Montagem e instalação de componentes."),
        ("Manutenção e limpeza", "Limpeza, manutenção preventiva e diagnóstico."),
        ("Upgrade de hardware", "Atualização e melhoria de componentes."),
        ("Software e sistemas", "Instalação e configuração de sistemas e programas.")
    ]

    servicos = [
        ("Montagem de PC", "Montagem completa do computador, com instalação e organização dos componentes.", "Montagem de computadores"),
        ("Instalação de componentes", "Instalação de peças como memória RAM, SSD e outros componentes compatíveis.", "Montagem de computadores"),
        ("Organização de cabos", "Organização dos cabos internos para melhorar a circulação de ar e o acabamento do computador.", "Montagem de computadores"),
        ("Instalação de fonte de alimentação", "Instalação e conexão da fonte, garantindo a alimentação adequada dos componentes.", "Montagem de computadores"),

        ("Limpeza interna", "Remoção de poeira e resíduos dos componentes internos para conservar o computador.", "Manutenção e limpeza"),
        ("Troca de pasta térmica", "Substituição da pasta térmica do processador para auxiliar na transferência de calor.", "Manutenção e limpeza"),
        ("Manutenção preventiva", "Verificação dos principais componentes para identificar possíveis problemas e prevenir falhas.", "Manutenção e limpeza"),
        ("Diagnóstico de problemas", "Análise do computador para identificar falhas de hardware ou software e orientar a solução.", "Manutenção e limpeza"),

        ("Instalação de memória RAM", "Instalação de módulos de memória RAM compatíveis para ampliar a capacidade do computador.", "Upgrade de hardware"),
        ("Instalação de SSD", "Instalação de unidade SSD para ampliar o armazenamento e possibilitar inicializações e carregamentos mais rápidos.", "Upgrade de hardware"),
        ("Troca de placa de vídeo", "Substituição da placa de vídeo por outro modelo compatível com o computador.", "Upgrade de hardware"),
        ("Atualização de processador", "Substituição do processador por um modelo compatível com a placa-mãe.", "Upgrade de hardware"),

        ("Instalação do Windows", "Instalação e configuração do sistema operacional Windows no computador.", "Software e sistemas"),
        ("Instalação de drivers", "Instalação e atualização de drivers para o funcionamento adequado dos componentes e periféricos.", "Software e sistemas"),
        ("Instalação de programas", "Instalação e configuração de programas conforme a necessidade do usuário.", "Software e sistemas"),

        ("Instalação de fans (ventoinhas)", "Instalação de ventoinhas para auxiliar na circulação de ar dentro do gabinete.", "Upgrade de hardware"),
        ("Instalação de water cooler", "Instalação de sistema de refrigeração líquida compatível com o gabinete e o processador.", "Upgrade de hardware"),
        ("Troca de gabinete", "Substituição do gabinete e transferência dos componentes para a nova estrutura.", "Upgrade de hardware"),
        ("Troca de placa-mãe", "Substituição da placa-mãe, considerando a compatibilidade com os demais componentes.", "Upgrade de hardware"),
    ]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO categorias (nome, descricao)
        VALUES (?, ?)
    """, categorias)

    for nome, descricao, categoria in servicos:
        cursor.execute("""
            SELECT id_categoria
            FROM categorias
            WHERE nome = ?
        """, (categoria,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError(f"Categoria não encontrada: {categoria}")

        categoria_id = resultado["id_categoria"]

        cursor.execute("""
            SELECT id_servico
            FROM servicos
            WHERE nome = ? AND categoria_id = ?
        """, (nome, categoria_id))

        servico_existente = cursor.fetchone()

        if servico_existente:
            cursor.execute("""
                UPDATE servicos
                SET descricao = ?
                WHERE id_servico = ?
            """, (descricao, servico_existente["id_servico"]))

        else:
            cursor.execute("""
                INSERT INTO servicos (nome, descricao, categoria_id)
                VALUES (?, ?, ?)
            """, (nome, descricao, categoria_id))
    conexao.commit()
    conexao.close()

    print("Categorias e serviços atualizados com sucesso!")


if __name__ == "__main__":
    cadastrar_dados()