#!/usr/bin/env python3
"""
OI — Startup otimizado para workspace pessoal
Atualiza ferramentas, valida ambiente e carrega contexto
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Fix encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Startup:
    def __init__(self):
        self.cwd = os.getcwd()
        self.project_root = self._find_project_root()
        self.memory_dir = Path.home() / ".claude" / "projects" / self._get_project_slug() / "memory"
        self.warnings = []
        self.errors = []
        self.updates = []

    def _find_project_root(self):
        """Encontra root do projeto (onde está .claude ou CLAUDE.md)"""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / ".claude").exists() or (parent / "CLAUDE.md").exists():
                return parent
        return current

    def _get_project_slug(self):
        """Converte path para slug compatible com .claude/projects/"""
        path = str(self.project_root).replace(":", "").replace("\\", "-")
        return path

    def print_header(self, text):
        """Printa header formatado"""
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")

    def print_section(self, num, text):
        """Printa seção numerada"""
        print(f"\n[{num}/8] {text}")
        print("-" * 70)

    def run_cmd(self, cmd, check=False, shell=True):
        """Executa comando e retorna output"""
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                cwd=self.cwd
            )
            if check and result.returncode != 0:
                self.errors.append(f"Comando falhou: {cmd}\n{result.stderr}")
            return result.stdout.strip(), result.returncode
        except Exception as e:
            self.errors.append(f"Erro ao executar {cmd}: {str(e)}")
            return "", 1

    def step_1_git_status(self):
        """1. Git Status"""
        self.print_section(1, "Git Status")

        # Branch atual
        branch, code = self.run_cmd("git branch --show-current")
        if code == 0:
            print(f"Branch: {branch or '(detached)'}")

            # Status
            status, _ = self.run_cmd("git status --short")
            if status:
                print(f"\nArquivos modificados:")
                for line in status.split("\n")[:10]:
                    print(f"  {line}")
                if len(status.split("\n")) > 10:
                    print(f"  ... e mais {len(status.split('\n')) - 10}")
            else:
                print("Nenhum arquivo modificado")

            # Últimos commits
            commits, _ = self.run_cmd("git log --oneline -3 2>/dev/null")
            if commits:
                print(f"\nÚltimos commits:")
                for line in commits.split("\n"):
                    print(f"  {line}")
        else:
            print("⚠️  Não é um repositório git")

    def step_2_atualizar_git(self):
        """2. Atualizar Git"""
        self.print_section(2, "Sincronizar com Remoto")

        # Apenas tenta se for repo git
        branch, code = self.run_cmd("git branch --show-current")
        if code != 0:
            print("Pulando (não é um repositório git)")
            return

        print("Fazendo fetch...")
        self.run_cmd("git fetch")

        # Check se há atualizações
        updates, _ = self.run_cmd("git log HEAD..origin/HEAD --oneline 2>/dev/null")
        if updates:
            print(f"\nAtualizações disponíveis no remoto:")
            for line in updates.split("\n")[:5]:
                print(f"  {line}")
        else:
            print("Branch está sincronizado com remoto")

    def step_3_memoria(self):
        """3. Memória do Projeto"""
        self.print_section(3, "Memória do Projeto")

        memory_file = self.memory_dir / "MEMORY.md"
        if memory_file.exists():
            with open(memory_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[:15]
                print(f"📌 Memória carregada ({len(lines)} linhas)")
                for line in lines:
                    print(f"  {line.rstrip()}")
        else:
            print("✗ Nenhuma memória encontrada")

    def step_4_claude_md(self):
        """4. CLAUDE.md"""
        self.print_section(4, "Instruções do Projeto (CLAUDE.md)")

        claude_file = self.project_root / "CLAUDE.md"
        if claude_file.exists():
            with open(claude_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"✓ CLAUDE.md carregado ({len(lines)} linhas)")

                # Valida avisos
                content = "".join(lines)
                if "token" in content.lower() or "credenciais" in content.lower():
                    self.warnings.append("CLAUDE.md menciona tokens/credenciais — validar .gitignore")
        else:
            print("ℹ️  Nenhum CLAUDE.md encontrado")

    def step_5_validar_dependencias(self):
        """5. Validar Dependências"""
        self.print_section(5, "Dependências do Ambiente")

        deps = {
            "python": "python --version",
            "git": "git --version",
            "node": "node --version",
            "npm": "npm --version",
        }

        self.versions = {}
        found = 0
        for name, cmd in deps.items():
            output, code = self.run_cmd(cmd)
            if code == 0:
                print(f"✓ {name.upper():10} {output}")
                self.versions[name] = output
                found += 1
            else:
                print(f"✗ {name.upper():10} não encontrado")

        print(f"\n{found}/{len(deps)} ferramentas disponíveis")

    def step_6_atualizar_python(self):
        """6. Atualizar Python Packages"""
        self.print_section(6, "Atualizar Python Packages")

        if "python" not in self.versions:
            print("Python não encontrado, pulando...")
            return

        print("Atualizando pip...")
        self.run_cmd("python -m pip install --upgrade pip")

        # Procura requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            print("\nInstalando requirements.txt...")
            code = self.run_cmd(f"pip install -r {req_file}")[1]
            if code == 0:
                self.updates.append("✓ Python packages atualizados")
            else:
                self.warnings.append("Erro ao instalar requirements.txt")
        else:
            print("ℹ️  Nenhum requirements.txt encontrado")

    def step_7_atualizar_node(self):
        """7. Atualizar Node Packages"""
        self.print_section(7, "Atualizar Node Packages")

        if "npm" not in self.versions:
            print("npm não encontrado, pulando...")
            return

        # Procura package.json
        pkg_file = self.project_root / "package.json"
        if pkg_file.exists():
            print("Instalando/atualizando node_modules...")
            code = self.run_cmd("npm install")[1]
            if code == 0:
                self.updates.append("✓ Node packages instalados")
            else:
                self.warnings.append("Erro ao instalar node packages")
        else:
            print("ℹ️  Nenhum package.json encontrado")

    def step_8_resumo_final(self):
        """8. Resumo do Projeto e Status Final"""
        self.print_section(8, "Resumo do Projeto")

        # Estrutura de diretórios
        dirs = [d for d in self.project_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
        print(f"Diretórios principais:")
        for d in sorted(dirs)[:10]:
            file_count = len(list(d.rglob("*")))
            print(f"  • {d.name}/ ({file_count} items)")

        # Skills
        skills_dir = self.project_root / ".claude" / "skills"
        if skills_dir.exists():
            skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
            print(f"\nSkills disponíveis: {', '.join(skills) if skills else '(nenhum)'}")

        # Status final
        self.print_header("STATUS FINAL")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp}")
        print(f"Projeto: {self.project_root.name}")
        print(f"CWD: {self.cwd}")

        if self.updates:
            print(f"\n✅ ATUALIZAÇÕES APLICADAS:")
            for update in self.updates:
                print(f"  {update}")

        if self.warnings:
            print(f"\n⚠️  AVISOS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  • {w}")

        if self.errors:
            print(f"\n❌ ERROS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  • {e}")

        print(f"\n{'='*70}")
        print("  Pronto para trabalhar! 🚀")
        print(f"{'='*70}\n")

    def run(self):
        """Executa todos os 8 passos"""
        self.print_header("OI — STARTUP OTIMIZADO")

        try:
            self.step_1_git_status()
            self.step_2_atualizar_git()
            self.step_3_memoria()
            self.step_4_claude_md()
            self.step_5_validar_dependencias()
            self.step_6_atualizar_python()
            self.step_7_atualizar_node()
            self.step_8_resumo_final()
        except KeyboardInterrupt:
            print("\n\n⚠️  Startup interrompido pelo usuário")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Erro durante startup: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    startup = Startup()
    startup.run()
