
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ServicosService, Servico, Categoria } from '../../servicos';

@Component({
  selector: 'app-catalogo',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './catalogo.html'
})
export class Catalogo implements OnInit {

  categorias: Categoria[] = [];
  servicos: Servico[] = [];
  termoPesquisa = '';

  carregando = true;
  erro = '';

  constructor(private servicosService: ServicosService) {}

  ngOnInit(): void {
    this.servicosService.listarCategorias().subscribe({
      next: (dados) => {
        this.categorias = dados;
      },
      error: (erro) => {
        console.error('Erro ao carregar categorias:', erro);
        this.erro = 'Não foi possível carregar as categorias.';
        this.carregando = false;
      }
    });

    this.servicosService.listarServicos().subscribe({
      next: (dados) => {
        this.servicos = dados;
        this.carregando = false;
      },
      error: (erro) => {
        console.error('Erro ao carregar serviços:', erro);
        this.erro = 'Não foi possível carregar os serviços.';
        this.carregando = false;
      }
    });
  }

  servicosPorCategoria(nomeCategoria: string): Servico[] {
    const pesquisa = this.termoPesquisa.trim().toLowerCase();

    return this.servicos.filter(servico => {
      const pertenceCategoria = servico.categoria === nomeCategoria;

      const correspondePesquisa =
        servico.nome.toLowerCase().includes(pesquisa) ||
        servico.descricao.toLowerCase().includes(pesquisa);

      return pertenceCategoria && correspondePesquisa;
    });
  }

  temServicosNaCategoria(nomeCategoria: string): boolean {
    return this.servicosPorCategoria(nomeCategoria).length > 0;
  }

  temResultadosPesquisa(): boolean {
    const pesquisa = this.termoPesquisa.trim().toLowerCase();

    return this.servicos.some(servico =>
      servico.nome.toLowerCase().includes(pesquisa) ||
      servico.descricao.toLowerCase().includes(pesquisa)
    );
  }
}
