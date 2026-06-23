#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar o dashboard de pedidos com dados atualizados
Uso: python3 gerar_dashboard.py Status_dos_Pedidos_Livoltek_-_Página1.csv
Gera: index.html (pronto para upload no GitHub)
"""

import csv
import json
import sys

def processar_csv(arquivo_csv):
    """Processa CSV e extrai dados únicos de pedidos"""
    data = []
    with open(arquivo_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    print(f"✓ Lidas {len(data)} linhas do CSV")
    
    # Filtrar e renomear colunas
    needed_cols = {
        'KAM': 'KAM',
        'PO (Relacionado)': 'Nº DO PEDIDO',
        'Customer (Relacionado)': 'CLIENTE',
        'Data Pedido Recebido': 'DATA RECEBIMENTO SM',
        'Data Pedido Completo': 'DATA RECEBIMENTO OFICIAL (PEDIDO COMPLETO)',
        'Data Aprovação no Totvs': 'DATA APROVAÇÃO NO TOTVS',
        'Data Envio Faturamento': 'DATA ENVIO PARA O PD',
        'Quais Pendências?': 'PENDÊNCIAS (MOTIVO)'
    }
    
    clean_data = []
    seen_pedidos = set()
    
    for row in data:
        pedido = row.get('PO (Relacionado)', '').strip()
        kam = row.get('KAM', '').strip()
        
        if pedido and kam and pedido not in seen_pedidos:
            clean_row = {}
            for orig_col, new_col in needed_cols.items():
                clean_row[new_col] = row.get(orig_col, '').strip()
            clean_data.append(clean_row)
            seen_pedidos.add(pedido)
    
    print(f"✓ Extraídos {len(clean_data)} pedidos únicos")
    return clean_data

def gerar_html(pedidos_data):
    """Gera HTML com dados embutidos"""
    data_json = json.dumps(pedidos_data, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Status de Pedidos - Livoltek</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; padding: 20px; }}
        .header {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; color: #2c3e50; }}
        .header p {{ color: #7f8c8d; font-size: 14px; }}
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .card.enviado {{ border-left: 4px solid #27ae60; }}
        .card.analise {{ border-left: 4px solid #f39c12; }}
        .card.aguardando {{ border-left: 4px solid #e74c3c; }}
        .card h3 {{ font-size: 32px; font-weight: bold; margin-bottom: 5px; }}
        .card p {{ color: #7f8c8d; font-size: 13px; }}
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .filters select {{
            padding: 8px 12px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
        }}
        .filters label {{ font-weight: 500; color: #2c3e50; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        th {{
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            font-size: 13px;
        }}
        tr:hover {{ background: #f9fafb; }}
        .status-enviado {{
            background: #d5f4e6;
            color: #27ae60;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-block;
        }}
        .status-analise {{
            background: #fef5e7;
            color: #f39c12;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-block;
        }}
        .status-aguardando {{
            background: #fadbd8;
            color: #e74c3c;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: 500;
            display: inline-block;
        }}
        .no-data {{ text-align: center; padding: 40px; color: #7f8c8d; }}
        .last-update {{ text-align: right; color: #7f8c8d; font-size: 12px; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Painel de Status de Pedidos</h1>
            <p>Livoltek - Sales Management | {len(pedidos_data)} pedidos</p>
        </div>

        <div class="cards-grid">
            <div class="card enviado">
                <h3 id="count-enviado">0</h3>
                <p>Enviado para Faturamento</p>
            </div>
            <div class="card analise">
                <h3 id="count-analise">0</h3>
                <p>Pendente de Envio</p>
            </div>
            <div class="card aguardando">
                <h3 id="count-aguardando">0</h3>
                <p>Em Aprovação</p>
            </div>
        </div>

        <div class="filters">
            <label for="filter-kam">KAM:</label>
            <select id="filter-kam"><option value="">Todos</option></select>
            <label for="filter-status">Status:</label>
            <select id="filter-status">
                <option value="">Todos</option>
                <option value="EM APROVAÇÃO">Em Aprovação</option>
                <option value="PENDENTE DE ENVIO PARA FATURAMENTO">Pendente de Envio</option>
                <option value="ENVIADO PARA FATURAMENTO">Enviado para Faturamento</option>
            </select>
        </div>

        <div id="table-container"></div>
        <div class="last-update" id="last-update"></div>
    </div>

    <script>
        // DADOS EMBUTIDOS - Atualizar toda semana
        const allData = {data_json};

        function calculateStatus(row) {{
            const dataRecebimento = row['DATA RECEBIMENTO SM'] || '';
            const dataPedidoCompleto = row['DATA RECEBIMENTO OFICIAL (PEDIDO COMPLETO)'] || '';
            const dataAprovacao = row['DATA APROVAÇÃO NO TOTVS'] || '';
            const dataEnvio = row['DATA ENVIO PARA O PD'] || '';

            if (!dataPedidoCompleto) return 'AGUARDANDO PEDIDO COMPLETO';
            if (dataRecebimento === dataPedidoCompleto && !dataAprovacao) return 'EM APROVAÇÃO';
            if (dataAprovacao && !dataEnvio) return 'PENDENTE DE ENVIO PARA FATURAMENTO';
            if (dataEnvio) return 'ENVIADO PARA FATURAMENTO. Consulte o time de PD';
            return 'AGUARDANDO PEDIDO COMPLETO';
        }}

        function getStatusClass(status) {{
            if (status.includes('ENVIADO')) return 'status-enviado';
            if (status === 'PENDENTE DE ENVIO PARA FATURAMENTO') return 'status-analise';
            return 'status-aguardando';
        }}

        function updateCounts() {{
            const enviado = allData.filter(r => calculateStatus(r).includes('ENVIADO')).length;
            const analise = allData.filter(r => calculateStatus(r) === 'PENDENTE DE ENVIO PARA FATURAMENTO').length;
            const aguardando = allData.filter(r => calculateStatus(r).includes('APROVAÇÃO') || calculateStatus(r).includes('AGUARDANDO')).length;

            document.getElementById('count-enviado').textContent = enviado;
            document.getElementById('count-analise').textContent = analise;
            document.getElementById('count-aguardando').textContent = aguardando;
        }}

        function populateKAMFilter() {{
            const kams = [...new Set(allData.map(r => r['KAM'] || '').filter(Boolean))].sort();
            const select = document.getElementById('filter-kam');
            kams.forEach(kam => {{
                const opt = document.createElement('option');
                opt.value = kam;
                opt.textContent = kam;
                select.appendChild(opt);
            }});
        }}

        function renderTable() {{
            const filterKam = document.getElementById('filter-kam').value;
            const filterStatus = document.getElementById('filter-status').value;

            let filtered = allData.map(row => ({{
                ...row,
                _status: calculateStatus(row)
            }}));

            if (filterKam) filtered = filtered.filter(r => r['KAM'] === filterKam);
            if (filterStatus) filtered = filtered.filter(r => r._status === filterStatus);

            if (filtered.length === 0) {{
                document.getElementById('table-container').innerHTML = '<div class="no-data">Nenhum pedido encontrado com esses filtros.</div>';
                return;
            }}

            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>KAM</th>
                            <th>Nº Pedido</th>
                            <th>Cliente</th>
                            <th>Receb. SM</th>
                            <th>Pedido Completo</th>
                            <th>Status</th>
                            <th>Pendências</th>
                            <th>Envio PD</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            filtered.forEach(row => {{
                const statusClass = getStatusClass(row._status);
                html += `
                    <tr>
                        <td>${{row['KAM'] || '--'}}</td>
                        <td><strong>${{row['Nº DO PEDIDO']}}</strong></td>
                        <td>${{row['CLIENTE'] || '--'}}</td>
                        <td>${{row['DATA RECEBIMENTO SM'] || '--'}}</td>
                        <td>${{row['DATA RECEBIMENTO OFICIAL (PEDIDO COMPLETO)'] || '--'}}</td>
                        <td><span class="${{statusClass}}">${{row._status}}</span></td>
                        <td>${{row['PENDÊNCIAS (MOTIVO)'] || '--'}}</td>
                        <td>${{row['DATA ENVIO PARA O PD'] || '--'}}</td>
                    </tr>
                `;
            }});

            html += '</tbody></table>';
            document.getElementById('table-container').innerHTML = html;
        }}

        document.getElementById('filter-kam').addEventListener('change', renderTable);
        document.getElementById('filter-status').addEventListener('change', renderTable);

        updateCounts();
        populateKAMFilter();
        renderTable();
        document.getElementById('last-update').textContent = 'Última atualização: ' + new Date().toLocaleString('pt-BR');
    </script>
</body>
</html>
"""
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 gerar_dashboard.py <arquivo.csv>")
        print("Exemplo: python3 gerar_dashboard.py Status_dos_Pedidos_Livoltek_-_Página1.csv")
        sys.exit(1)
    
    arquivo_csv = sys.argv[1]
    
    try:
        pedidos_data = processar_csv(arquivo_csv)
        html = gerar_html(pedidos_data)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ Dashboard gerado: index.html ({len(html)} bytes)")
        print(f"✓ Pronto para upload no GitHub")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
