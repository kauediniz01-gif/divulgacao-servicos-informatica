
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface Categoria {
  id_categoria: number;
  nome: string;
  descricao: string | null;
}

export interface Servico {
  id_servico: number;
  nome: string;
  descricao: string;
  categoria_id: number;
  categoria: string;
}

@Injectable({
  providedIn: 'root'
})
export class ServicosService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  listarCategorias(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.apiUrl}/categorias`);
  }

  listarServicos(): Observable<Servico[]> {
    return this.http.get<Servico[]>(`${this.apiUrl}/servicos`);
  }
}
