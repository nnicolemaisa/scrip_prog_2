import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

class PDB_Separador:
    def __init__(self, pdb_path=None):
        self.pdb_path = pdb_path
        self.chains = {}
        self.ligand_lines = []

    def p_chains(self):
        self.chains.clear()
        self.ligand_lines.clear()

        with open(self.pdb_path, 'r') as file:
            for line in file:
                if line.startswith("HETATM"):
                    self.ligand_lines.append(line)
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    chain_id = line[21]
                    if chain_id not in self.chains:
                        self.chains[chain_id] = []
                    self.chains[chain_id].append(line)

    def save_chains(self, output_prefix="chain_"):
        downloads_path = Path.home() / "Downloads"
        saved_files = []
        for chain_id, lines in self.chains.items():
            filename = downloads_path / f"{output_prefix}{chain_id}.pdb"
            with open(filename, 'w') as outfile:
                outfile.writelines(lines)
                outfile.write("END\n")
            saved_files.append(str(filename))
 

    def save_chains(self, output_prefix="_chain_"):
        downloads_path = Path.home() / "Downloads"
        base= os.path.splitext(os.path.basename(self.pdb_path))[0]  # pega o nome sem extensão
        saved_files = []
        for chain_id, lines in self.chains.items():
            filename = downloads_path / f"{base}{output_prefix}{chain_id}.pdb"  # ex: proteina1_chain_A.pdb
            with open(filename, 'w') as outfile:
                outfile.writelines(lines)
                outfile.write("END\n")
                saved_files.append(str(filename))

        return saved_files

    def save_ligands(self, ligand_filename=None):
        if self.ligand_lines:
            downloads_path = Path.home() / "Downloads"
            if ligand_filename is None:
                base_name = os.path.splitext(os.path.basename(self.pdb_path))[0]
                ligand_filename = f"{base_name}_ligand.pdb"
            ligand_path = downloads_path / ligand_filename
            with open(ligand_path, 'w') as ligand_file:
                ligand_file.writelines(self.ligand_lines)
                ligand_file.write("END\n")
            return str(ligand_path)
        return None

    def run(self):
        if not self.pdb_path:
            raise ValueError("Nenhum caminho de arquivo PDB fornecido.")
        self.p_chains()
        chains_files = self.save_chains()
        ligand_file = self.save_ligands()
        return chains_files, ligand_file, self.chains


class InterfaceSeparadora(PDB_Separador):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Editor de .pdb")

        # Instruções
        tk.Label(self.root, text='Cole o caminho para o arquivo .pdb para processa-lo ou utilize o botão a baixo para selecionar:').pack(pady=10)

        # Entrada do caminho
        self.entrada = tk.Entry(self.root, width=60)
        self.entrada.pack()

        # Botões
        tk.Button(self.root, text='Selecionar Arquivo', command=self.selecionar_arquivo).pack(pady=5)
        tk.Button(self.root, text='Executar Separação', command=self.executar_separacao).pack(pady=5)
        tk.Button(self.root, text='Sair', command=self.root.destroy).pack(pady=5)

        # Área de resultado
        self.resultado = tk.Text(self.root, height=10, width=70)
        self.resultado.pack(pady=10)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDB", "*.pdb")])
        if caminho:
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, caminho)
            self.pdb_path = caminho

    def executar_separacao(self):
        self.resultado.delete("1.0", tk.END)

        if not self.pdb_path:
            messagebox.showerror("Erro", "Nenhum arquivo PDB selecionado.")
            return

        try:
            chain_files, ligand_file, chains = self.run()
            self.resultado.insert(tk.END, f"Arquivo processado: {os.path.basename(self.pdb_path)}\n\n")
            self.resultado.insert(tk.END, " Cadeias encontradas:\n")
            for chain_id, linhas in chains.items():
                self.resultado.insert(tk.END, f" - Cadeia {chain_id}: {len(linhas)} linhas salvas em chain_{chain_id}.pdb\n")
            if ligand_file:
                self.resultado.insert(tk.END, f"\n Ligantes salvos em: {ligand_file}")
            else:
                self.resultado.insert(tk.END, "\n Nenhum ligante (HETATM) encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# Executar
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x450")
    app = InterfaceSeparadora(root)
    root.mainloop()


