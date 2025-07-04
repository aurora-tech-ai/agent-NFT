#!/usr/bin/env python3
"""
Hypnotic NFT Agent v3.0 - Clean Architecture
Gera NFTs e inicia marketplace automaticamente
"""

import os
import json
import time
import random
import hashlib
import requests
import subprocess
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import sys

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@dataclass
class NFTArtwork:
    name: str
    description: str
    style: str
    rarity: str
    price: float
    attributes: Dict[str, any]
    svg_code: str
    
class HypnoticNFTAgent:
    def __init__(self):
        self.model = "deepseek-reasoner"
        self.max_tokens = 20000
        
        # Estrutura limpa de diretórios
        self.nfts_dir = Path.cwd() / "nfts"
        self.nfts_dir.mkdir(exist_ok=True)
        
        print(f"📁 Diretório NFTs: {self.nfts_dir}")
        
        # Contadores
        self.nft_counter = 0
        self.session_start = time.time()
        self.session_cost = 0
        self.marketplace_process = None
        
        # Estilos artísticos
        self.art_styles = [
            "Hypnotic Spirals", "Psychedelic Mandala", "Kaleidoscope Dreams",
            "Fractal Evolution", "Sacred Geometry Motion", "DMT Visual Journey",
            "Quantum Particles", "Neural Network", "Data Flow Streams",
            "Holographic Interface", "Neon Circuit Board", "Digital DNA Helix",
            "Bioluminescent Ocean", "Crystal Formation", "Liquid Metal Flow",
            "Aurora Borealis", "Plasma Energy", "Living Coral Reef",
            "Generative Waves", "Particle Symphony", "Color Transitions",
            "Geometric Metamorphosis", "Perlin Noise Flow", "Voronoi Evolution",
            "Galaxy Formation", "Black Hole", "Nebula Birth", "Solar Flare",
            "Glitch Cascade", "Digital Decay", "Reality Fragmentation",
            "Third Eye Activation", "Chakra Flow", "Kundalini Rising",
            "4D Hypercube", "Tesseract", "Klein Bottle", "Time Crystal"
        ]
        
        # Raridades e preços
        self.rarity_config = {
            "Common": {"chance": 0.40, "base_price": 40, "multiplier": 1},
            "Rare": {"chance": 0.30, "base_price": 100, "multiplier": 1.5},
            "Epic": {"chance": 0.20, "base_price": 250, "multiplier": 2},
            "Legendary": {"chance": 0.10, "base_price": 500, "multiplier": 3}
        }
        
    def start_marketplace(self):
        """Inicia o marketplace em background"""
        def run_marketplace():
            try:
                print("\n🛍️ Iniciando Marketplace...")
                self.marketplace_process = subprocess.Popen(
                    [sys.executable, "marketplace.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Aguarda marketplace iniciar
                time.sleep(3)
                print("✅ Marketplace rodando em http://localhost:5000")
                
            except Exception as e:
                print(f"❌ Erro ao iniciar marketplace: {e}")
        
        # Executa em thread separada
        marketplace_thread = threading.Thread(target=run_marketplace, daemon=True)
        marketplace_thread.start()
    
    def generate_unique_name(self) -> str:
        """Gera nome único e criativo"""
        prefixes = ["Ethereal", "Quantum", "Cosmic", "Neural", "Hypnotic", 
                   "Celestial", "Digital", "Infinite", "Prismatic", "Temporal"]
        subjects = ["Vortex", "Portal", "Nexus", "Matrix", "Flow", "Dream", 
                   "Vision", "Pulse", "Wave", "Spiral", "Realm", "Echo"]
        
        return f"{random.choice(prefixes)} {random.choice(subjects)}"
    
    def determine_rarity(self) -> str:
        """Determina raridade baseada em probabilidades"""
        rand = random.random()
        cumulative = 0
        for rarity, config in self.rarity_config.items():
            cumulative += config["chance"]
            if rand <= cumulative:
                return rarity
        return "Common"
    
    def calculate_price(self, rarity: str, complexity: int) -> float:
        """Calcula preço baseado em raridade e complexidade"""
        config = self.rarity_config[rarity]
        base = config["base_price"]
        multiplier = config["multiplier"]
        
        # Ajusta por complexidade (1-10)
        complexity_bonus = 1 + (complexity / 20)
        
        return round(base * multiplier * complexity_bonus, 2)
    
    def estimate_cost(self, tokens: int) -> float:
        """Estima custo da geração"""
        cost_per_1k = 0.014
        current_hour = time.gmtime().tm_hour
        
        # Desconto horário brasileiro
        if (current_hour >= 16) or (current_hour <= 0):
            cost_per_1k *= 0.25
            
        return (tokens / 1000) * cost_per_1k
    
    def generate_artwork(self) -> NFTArtwork:
        """Gera uma obra de arte NFT"""
        style = random.choice(self.art_styles)
        rarity = self.determine_rarity()
        name = self.generate_unique_name()
        
        # Complexidade por raridade
        complexity_map = {
            "Common": {"min_animations": 6, "complexity": 6, "colors": 4},
            "Rare": {"min_animations": 10, "complexity": 7, "colors": 6},
            "Epic": {"min_animations": 15, "complexity": 8, "colors": 8},
            "Legendary": {"min_animations": 20, "complexity": 10, "colors": 10}
        }
        
        reqs = complexity_map[rarity]
        
        # Paletas de cores por estilo
        color_palettes = {
            "Hypnotic Spirals": ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF"],
            "Psychedelic Mandala": ["#FF0080", "#FF8C00", "#FFD700", "#00CED1", "#9400D3"],
            "Quantum Particles": ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF1493"],
            "Neural Network": ["#00D9FF", "#00FF88", "#FF0099", "#FFD300", "#9D00FF"],
            "Sacred Geometry Motion": ["#FFD700", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"],
            "Neon Circuit Board": ["#39FF14", "#FF1493", "#00CED1", "#FFD700", "#FF00FF"],
            "Galaxy Formation": ["#E94B3C", "#EE7879", "#F6D55C", "#3CAEA3", "#20639B"],
            "Aurora Borealis": ["#00FF41", "#00D4FF", "#FF006E", "#FFDD00", "#FF00DC"]
        }
        
        # Seleciona paleta ou gera uma vibrante
        base_colors = color_palettes.get(style, [
            f"#{random.randint(128,255):02X}{random.randint(0,128):02X}{random.randint(128,255):02X}",
            f"#{random.randint(0,128):02X}{random.randint(128,255):02X}{random.randint(128,255):02X}",
            f"#{random.randint(128,255):02X}{random.randint(128,255):02X}{random.randint(0,128):02X}",
            f"#{random.randint(255,255):02X}{random.randint(0,128):02X}{random.randint(128,255):02X}",
            f"#{random.randint(128,255):02X}{random.randint(0,255):02X}{random.randint(200,255):02X}"
        ])
        
        prompt = f"""
Você é um MESTRE em criar arte SVG SURREAL, HIPNOTIZANTE e PROFUNDAMENTE ANIMADA.

CONTEXTO:
- Nome da obra: {name}
- Estilo: {style}
- Raridade: {rarity}
- Cores base sugeridas: {', '.join(base_colors[:reqs['colors']])}

REQUISITOS TÉCNICOS OBRIGATÓRIOS:
1. ViewBox: EXATAMENTE viewBox="0 0 1000 1000"
2. Background: Cor sólida ou gradiente radial/linear (NUNCA transparente)
3. Mínimo de {reqs['min_animations']} animações DIFERENTES e SINCRONIZADAS
4. TODAS as animações com repeatCount="indefinite"
5. Duração das animações: Varie entre 3s e 30s para criar polirritmia hipnótica
6. Use calcMode="spline" com keySplines para movimentos orgânicos

TÉCNICAS DE ANIMAÇÃO OBRIGATÓRIAS (use TODAS):

1. ROTAÇÕES HIPNÓTICAS:
   <animateTransform attributeName="transform" type="rotate" 
    from="0 500 500" to="360 500 500" dur="20s" repeatCount="indefinite"/>
   - Varie: direção (360 ou -360), centro de rotação, duração

2. MORPHING DE FORMAS:
   <animate attributeName="d" values="path1;path2;path3;path1" 
    dur="10s" repeatCount="indefinite" calcMode="spline" 
    keySplines="0.5 0 0.5 1;0.5 0 0.5 1"/>
   - Transforme círculos em estrelas, quadrados em espirais

3. PULSAÇÕES ORGÂNICAS:
   <animate attributeName="r" values="50;80;50" dur="4s" 
    repeatCount="indefinite" calcMode="spline"/>
   - Aplique em raios, larguras, alturas

4. ONDULAÇÕES DE COR:
   <animate attributeName="fill" values="cor1;cor2;cor3;cor1" 
    dur="8s" repeatCount="indefinite"/>
   - Use nas cores base fornecidas

5. MOVIMENTOS EM PATHS:
   <animateMotion dur="15s" repeatCount="indefinite">
     <mpath href="#pathId"/>
   </animateMotion>
   - Crie paths sinuosos, espirais, lemniscatas

6. OPACIDADE FANTASMAGÓRICA:
   <animate attributeName="opacity" values="0;1;0" 
    dur="6s" repeatCount="indefinite"/>

7. TRANSFORMAÇÕES DE ESCALA:
   <animateTransform attributeName="transform" type="scale" 
    values="1;1.5;1" dur="7s" repeatCount="indefinite" additive="sum"/>

8. FILTROS DINÂMICOS:
   - Use feTurbulence com baseFrequency animado
   - feGaussianBlur com stdDeviation variável
   - feDisplacementMap para distorções líquidas

ELEMENTOS VISUAIS OBRIGATÓRIOS PARA {style}:
{self._get_style_specific_requirements(style)}

ESTRUTURA SURREAL OBRIGATÓRIA:
1. PROFUNDIDADE: Mínimo 5 camadas com diferentes velocidades (parallax)
2. ELEMENTOS IMPOSSÍVEIS: Geometrias não-euclidianas, ilusões de ótica
3. FLUXO LÍQUIDO: Tudo deve fluir como se estivesse submerso
4. SINCRONIZAÇÃO: Crie "momentos" onde várias animações se alinham
5. SURPRESAS VISUAIS: Elementos que aparecem/desaparecem periodicamente

EXEMPLO DE ESTRUTURA SVG:
```svg
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradientes animados -->
    <radialGradient id="grad1">
      <stop offset="0%" stop-color="#FF006E">
        <animate attributeName="stop-color" values="#FF006E;#FB5607;#FF006E" dur="5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#3A86FF">
        <animate attributeName="stop-color" values="#3A86FF;#8338EC;#3A86FF" dur="7s" repeatCount="indefinite"/>
      </stop>
    </radialGradient>
    
    <!-- Filtros complexos -->
    <filter id="liquid">
      <feTurbulence baseFrequency="0.02" numOctaves="3">
        <animate attributeName="baseFrequency" values="0.02;0.05;0.02" dur="10s" repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" scale="20"/>
    </filter>
    
    <!-- Paths para movimento -->
    <path id="spiral" d="M500,500 Q600,400 500,300 T400,400 T500,500" opacity="0"/>
  </defs>
  
  <!-- Background animado -->
  <rect width="1000" height="1000" fill="url(#grad1)"/>
  
  <!-- Camadas com diferentes velocidades e filtros -->
  <!-- ... elementos surreais aqui ... -->
</svg>
```

IMPORTANTE PARA {rarity}:
- Common: Foco em loops perfeitos e harmonia visual
- Rare: Adicione elementos que quebram o padrão periodicamente  
- Epic: Múltiplas dimensões visuais interagindo
- Legendary: Transcenda a percepção normal, crie portais visuais

PROIBIDO:
- Elementos estáticos (TUDO deve se mover)
- Animações abruptas (use sempre easing/splines)
- Cores muito escuras ou muito claras (mantenha vibrante)
- Repetições óbvias (varie durações para criar polirritmia)
- SVG com erro de sintaxe

Retorne um JSON VÁLIDO:
{{
    "artwork_name": "{name} (ou uma variação poética)",
    "description": "Descrição surreal e poética que capture a essência hipnótica da obra (3-4 frases)",
    "svg_code": "<!-- SVG COMPLETO E VÁLIDO COM TODAS AS ANIMAÇÕES -->",
    "attributes": {{
        "animation_count": {reqs['min_animations']} (número exato de animações),
        "complexity": {reqs['complexity']},
        "hypnotic_factor": número de 1-10,
        "primary_colors": {base_colors[:reqs['colors']]},
        "loop_duration": duração do loop mestre em segundos,
        "special_features": ["feature1", "feature2", "feature3"]
    }}
}}

LEMBRE-SE: Esta arte deve ser um PORTAL VISUAL que HIPNOTIZA e TRANSCENDE. Cada elemento deve DANÇAR em harmonia surreal. O observador deve sentir que está olhando para outra dimensão!
"""
        
        try:
            print(f"\n🎨 Gerando NFT #{self.nft_counter + 1}")
            print(f"   Raridade: {rarity}")
            print(f"   Estilo: {style}")
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Você é um gênio criativo especializado em arte SVG surreal e hipnotizante. Você domina completamente a sintaxe SVG, animações SMIL, filtros, gradientes e transformações. Suas criações são portais visuais para outras dimensões. SEMPRE retorne JSON válido com SVG sintaticamente perfeito."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": 0.9,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            result = json.loads(response.json()['choices'][0]['message']['content'])
            
            # Validação rigorosa
            svg_code = result.get("svg_code", "")
            if not svg_code or len(svg_code) < 500:
                raise ValueError("SVG muito curto")
            
            if not all(tag in svg_code for tag in ["<svg", "<animate", "viewBox=\"0 0 1000 1000\""]):
                raise ValueError("SVG incompleto ou malformado")
            
            animation_count = svg_code.count("<animate")
            if animation_count < reqs['min_animations']:
                raise ValueError(f"Poucas animações: {animation_count} < {reqs['min_animations']}")
            
            # Calcula custo
            tokens = response.json().get('usage', {}).get('total_tokens', 0)
            cost = self.estimate_cost(tokens)
            self.session_cost += cost
            
            # Calcula preço de venda
            complexity = result["attributes"].get("complexity", reqs['complexity'])
            price = self.calculate_price(rarity, complexity)
            
            artwork = NFTArtwork(
                name=result["artwork_name"],
                description=result["description"],
                style=style,
                rarity=rarity,
                price=price,
                attributes=result["attributes"],
                svg_code=svg_code
            )
            
            print(f"   ✅ Gerado: {artwork.name}")
            print(f"   🎬 Animações: {animation_count}")
            print(f"   💰 Preço: ${price}")
            print(f"   💸 Custo: ${cost:.3f}")
            
            return artwork
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            raise
    
    def _get_style_specific_requirements(self, style: str) -> str:
        """Requisitos específicos detalhados para cada estilo"""
        requirements = {
            "Hypnotic Spirals": """
- ESPIRAIS LOGARÍTMICAS em múltiplas camadas rotacionando em velocidades diferentes
- Use a fórmula: r = a * e^(b*θ) para criar espirais perfeitas
- Mínimo 5 espirais com centros deslocados criando interferência visual
- Gradientes radiais animados do centro para as bordas
- Efeito de "túnel infinito" com escala diminuindo ao centro""",
            
            "Psychedelic Mandala": """
- SIMETRIA RADIAL perfeita com 6, 8 ou 12 eixos
- Padrões fractais recursivos em cada seção
- Rotação caleidoscópica com diferentes camadas em contra-rotação  
- Morphing entre formas geométricas sagradas (flor da vida, sri yantra)
- Cores complementares pulsando em harmonia""",
            
            "Quantum Particles": """
- SISTEMA DE PARTÍCULAS com mínimo 50 elementos
- Movimento browniano aleatório mas suave (use animate com valores múltiplos)
- Conexões dinâmicas entre partículas próximas (linhas que aparecem/desaparecem)
- Efeito de "entanglement" - partículas que se movem em sincronia
- Halos de luz pulsantes em cada partícula""",
            
            "Neural Network": """
- REDE DE NEURÔNIOS com nós pulsantes conectados
- Sinais viajando através das conexões (use animateMotion)
- Ativação em cascata - quando um nó pulsa, ativa os próximos
- Estrutura em camadas com profundidade visual (perspective)
- Sinapses que se formam e dissolvem dinamicamente""",
            
            "Sacred Geometry Motion": """
- FORMAS GEOMÉTRICAS SAGRADAS morphing entre si
- Proporção áurea (1.618) em todos os elementos
- Tetraedro → Cubo → Octaedro → Dodecaedro → Icosaedro
- Merkaba rotacionando em múltiplos eixos
- Sobreposição criando padrões de interferência""",
            
            "Galaxy Formation": """
- BRAÇOS ESPIRAIS de galáxia em rotação lenta
- Nebulosas com cores vibrantes e filtros de turbulência  
- Estrelas nascendo e morrendo (opacity e scale animations)
- Buraco negro central com efeito de distorção (feDisplacementMap)
- Poeira cósmica com partículas flutuantes""",
            
            "Aurora Borealis": """
- ONDAS DE LUZ fluindo verticalmente
- Gradientes lineares animados simulando cortinas de luz
- Movimento ondulatório com paths sinusoidais
- Reflexo espelhado na parte inferior (como sobre água)
- Partículas de luz subindo suavemente"""
        }
        
        return requirements.get(style, f"""
- ELEMENTOS CARACTERÍSTICOS do estilo {style}
- Movimento fluido e orgânico constante
- Interação visual entre todos os elementos
- Profundidade através de camadas e transparências
- Surpresas visuais que aparecem periodicamente""")
    
    def save_nft_package(self, artwork: NFTArtwork) -> str:
        """Salva NFT em estrutura limpa"""
        # Cria pasta única para o NFT
        timestamp = int(time.time())
        folder_name = f"{artwork.rarity.lower()}_{artwork.name.replace(' ', '_')}_{timestamp}"
        nft_path = self.nfts_dir / folder_name
        nft_path.mkdir(exist_ok=True)
        
        # 1. Salva SVG original
        svg_file = nft_path / "artwork.svg"
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(artwork.svg_code)
        
        # 2. Cria metadata.json
        metadata = {
            "id": hashlib.md5(f"{artwork.name}{timestamp}".encode()).hexdigest()[:8],
            "name": artwork.name,
            "description": artwork.description,
            "price": artwork.price,
            "rarity": artwork.rarity,
            "style": artwork.style,
            "animation_count": artwork.attributes.get("animation_count", 10),
            "complexity": artwork.attributes.get("complexity", 7),
            "hypnotic_factor": artwork.attributes.get("hypnotic_factor", 8),
            "primary_colors": artwork.attributes.get("primary_colors", []),
            "loop_duration": artwork.attributes.get("loop_duration", 20),
            "special_features": artwork.attributes.get("special_features", []),
            "created_at": datetime.now().isoformat(),
            "folder": folder_name
        }
        
        metadata_file = nft_path / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        # 3. Cria preview.html protegido
        preview_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{artwork.name} - NFT Preview</title>
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }}
        
        body {{ 
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            position: relative;
        }}
        
        .container {{
            width: 90vmin;
            height: 90vmin;
            max-width: 800px;
            max-height: 800px;
            position: relative;
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        svg {{
            width: 100%;
            height: 100%;
            pointer-events: none;
        }}
        
        .watermark {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            pointer-events: none;
        }}
        
        .info {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-family: Arial, sans-serif;
        }}
        
        .info h3 {{
            margin: 0 0 5px 0;
            color: #333;
            font-size: 18px;
        }}
        
        .info p {{
            margin: 0;
            color: #666;
            font-size: 14px;
        }}
        
        .rarity {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .rarity.common {{ background: #e5e7eb; color: #374151; }}
        .rarity.rare {{ background: #dbeafe; color: #1e40af; }}
        .rarity.epic {{ background: #e9d5ff; color: #6b21a8; }}
        .rarity.legendary {{ background: #fed7aa; color: #92400e; }}
    </style>
</head>
<body oncontextmenu="return false;">
    <div class="container">
        {artwork.svg_code}
        <div class="watermark">PREVIEW</div>
        <div class="info">
            <h3>{artwork.name}</h3>
            <p>{artwork.style}</p>
            <span class="rarity {artwork.rarity.lower()}">{artwork.rarity}</span>
        </div>
    </div>
    
    <script>
        // Proteções
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        document.addEventListener('dragstart', e => e.preventDefault());
        
        document.addEventListener('keydown', e => {{
            if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {{
                e.preventDefault();
                return false;
            }}
        }});
    </script>
</body>
</html>"""
        
        preview_file = nft_path / "preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(preview_html)
        
        print(f"   📦 Salvo em: nfts/{folder_name}/")
        
        return folder_name
    
    def run_generation_loop(self, count: Optional[int] = None):
        """Loop principal de geração"""
        generated = 0
        
        print("\n🚀 Iniciando geração de NFTs...")
        print("🛑 Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                if count and generated >= count:
                    break
                
                self.nft_counter += 1
                generated += 1
                
                # Gera NFT
                artwork = self.generate_artwork()
                
                # Salva pacote
                folder = self.save_nft_package(artwork)
                
                print(f"   ⏱️ Total gerados: {self.nft_counter}")
                print(f"   💵 Gasto acumulado: ${self.session_cost:.2f}\n")
                
                # Pausa entre gerações
                if not count or generated < count:
                    time.sleep(3)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Geração interrompida!")
        
        return generated

def main():
    """Função principal"""
    print("="*60)
    print("🌀 HYPNOTIC NFT SYSTEM v3.0")
    print("💎 Clean Architecture Edition")
    print("="*60)
    
    # Verifica configuração
    if not DEEPSEEK_API_KEY:
        print("\n❌ Configure DEEPSEEK_API_KEY no arquivo .env")
        return
    
    if not os.getenv('STRIPE_SECRET_KEY'):
        print("\n⚠️ Configure STRIPE_SECRET_KEY no .env para pagamentos")
    
    agent = HypnoticNFTAgent()
    
    # Inicia marketplace automaticamente
    agent.start_marketplace()
    time.sleep(2)
    
    # Menu de opções
    print("\n📋 Opções de geração:")
    print("1. Gerar continuamente (infinito)")
    print("2. Gerar quantidade específica")
    print("3. Gerar apenas 1 NFT de teste")
    
    choice = input("\nEscolha (1-3): ").strip()
    
    if choice == "2":
        count = int(input("Quantos NFTs? "))
    elif choice == "3":
        count = 1
    else:
        count = None
    
    # Inicia geração
    total = agent.run_generation_loop(count)
    
    # Resumo final
    print(f"\n📊 RESUMO DA SESSÃO")
    print(f"="*40)
    print(f"NFTs gerados: {total}")
    print(f"Custo total: ${agent.session_cost:.2f}")
    print(f"Custo médio: ${agent.session_cost/max(total,1):.2f}")
    print(f"\n✨ Marketplace continua rodando em http://localhost:5000")
    print("💡 Use Ctrl+C para encerrar tudo")
    
    # Mantém o programa rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Encerrando sistema...")
        if agent.marketplace_process:
            agent.marketplace_process.terminate()

if __name__ == "__main__":
    main()