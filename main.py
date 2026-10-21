from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup 
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from datetime import datetime

# Definição das cores em Hexadecimal
COR_VERDE = "#08C853"
COR_AZUL = "#2962FF"  # Corrigido o hexadecimal inválido anterior
COR_CINZA = "#202020"

class TelaVendas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        
        self.total_geral = 0.0
        self.produtos_atuais = []

        # Tenta mostrar o Logotipo, se não existir, mostra o Texto
        try:
            # Força o erro se o ficheiro não existir para ativar o except
            import os
            if not os.path.exists('logo_tf.png'):
                raise FileNotFoundError
            
            logo = Image(source='logo_tf.png', size_hint_y=None, height=110)
            self.add_widget(logo)
        except:
            titulo = Label(
                text="[b]TECNO FREITAS[/b]", 
                markup=True, 
                font_size=25, 
                color=get_color_from_hex(COR_VERDE), 
                size_hint_y=None, 
                height=50
            )
            self.add_widget(titulo)

        # Subtítulo
        sub = Label(text="Sistema de Vendas", font_size=14, color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=20)
        self.add_widget(sub)

        # Campos de Entrada (Inputs)
        self.nome_input = TextInput(
            hint_text='Nome do produto', multiline=False, size_hint_y=None, height=45, 
            background_color=get_color_from_hex(COR_CINZA), foreground_color=(1, 1, 1, 1), padding=12
        )
        
        self.preco_input = TextInput(
            hint_text='Preço em Kz', multiline=False, input_filter='float', size_hint_y=None, height=45, 
            background_color=get_color_from_hex(COR_CINZA), foreground_color=(1, 1, 1, 1), padding=12
        )
        
        self.qtd_input = TextInput(
            hint_text='Quantidade', multiline=False, input_filter='int', size_hint_y=None, height=45, 
            background_color=get_color_from_hex(COR_CINZA), foreground_color=(1, 1, 1, 1), padding=12
        )

        self.add_widget(self.nome_input)
        self.add_widget(self.preco_input)
        self.add_widget(self.qtd_input)

        # Lista de Produtos (Container)
        self.lista_produtos = BoxLayout(orientation='vertical', spacing=4, size_hint_y=None)
        self.lista_produtos.bind(minimum_height=self.lista_produtos.setter('height'))
        self.add_widget(self.lista_produtos)

        # Rótulo do Total
        self.total_label = Label(
            text='TOTAL: 0.00 Kz', font_size=22, bold=True, 
            color=get_color_from_hex(COR_VERDE), size_hint_y=None, height=45
        )
        self.add_widget(self.total_label)

        # Botão Adicionar
        btn_add = Button(
            text='ADICIONAR PRODUTO', background_color=get_color_from_hex(COR_AZUL), 
            size_hint_y=None, height=50, bold=True, background_normal=''
        )
        btn_add.bind(on_press=self.adicionar_produto)
        self.add_widget(btn_add)

        # Botão Finalizar
        btn_final = Button(
            text='FINALIZAR VENDA', background_color=get_color_from_hex(COR_VERDE), 
            size_hint_y=None, height=50, bold=True, background_normal=''
        )
        btn_final.bind(on_press=self.finalizar_venda)
        self.add_widget(btn_final)

    def adicionar_produto(self, instance):
        # Lógica para adicionar produto
        nome = self.nome_input.text
        preco_txt = self.preco_input.text
        qtd_txt = self.qtd_input.text

        if nome and preco_txt and qtd_txt:
            preco = float(preco_txt)
            qtd = int(qtd_txt)
            subtotal = preco * qtd
            self.total_geral += subtotal
            
            # Adiciona linha visual do produto
            item_text = f"{nome} x{qtd} - {subtotal:.2f} Kz"
            self.lista_produtos.add_widget(Label(text=item_text, size_hint_y=None, height=30))
            
            # Atualiza o total global
            self.total_label.text = f"TOTAL: {self.total_geral:.2f} Kz"
            
            # Limpa os campos
            self.nome_input.text = ''
            self.preco_input.text = ''
            self.qtd_input.text = ''

    def finalizar_venda(self, instance):
        # Lógica para finalizar a venda e exibir um Popup
        conteudo = BoxLayout(orientation='vertical', padding=10, spacing=10)
        conteudo.add_widget(Label(text=f"Venda concluída com sucesso!\nTotal Pago: {self.total_geral:.2f} Kz"))
        
        btn_fechar = Button(text="Ok", size_hint_y=None, height=40)
        conteudo.add_widget(btn_fechar)
        
        popup = Popup(title="Sucesso", content=conteudo, size_hint=(None, None), size=(300, 200))
        btn_fechar.bind(on_press=popup.dismiss)
        popup.open()
        
        # Reseta o estado da tela
        self.lista_produtos.clear_widgets()
        self.total_geral = 0.0
        self.total_label.text = 'TOTAL: 0.00 Kz'

class VendasApp(App):
    def build(self):
        return TelaVendas()

if __name__ == '__main__':
    VendasApp().run()
