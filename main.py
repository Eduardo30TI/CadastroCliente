from Acentos import Acentuacao
from CNPJ import CNPJ
from Gmail import Mail
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import time
import json
import os
from glob import glob
import pandas as pd
from datetime import datetime
import shutil

mail=Mail()

def main():

    placeholder=st.empty()

    temp_dict=dict()

    with placeholder.container():

        st.header('Cadastro de Cliente')
        st.markdown('----')

        temp_dict['consultor']=st.text_input('E-mail Consultor')
        
        col1,col2=st.columns(2)
        temp_dict['cnpj']=col1.text_input(label='CNPJ',placeholder='Digite o CNPJ')
        
        if len(temp_dict['cnpj'])>0:

            if len(temp_dict['cnpj'])>14 or len(temp_dict['cnpj'])<14:

                mensagem=st.warning('CNPJ invalido')
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                cnpj=CNPJ(temp_dict['cnpj'])
                dados=cnpj.GetCNPJ()

                for c in ['cep','numero']:

                    for r in ['.','-']:

                        dados[c]=str(dados[c]).replace(r,'')

                        pass

                    pass

                temp_dict['razao_social']=st.text_input('Razão Social',value=dados['nome'],disabled=True).upper()
                temp_dict['fantasia']=st.text_input('Nome Fantasia',value=dados['fantasia'],disabled=True).upper()
                temp_dict['situacao']=col2.text_input('Situação',value=dados['situacao'],disabled=True).upper()

                temp_dict['logradouro']=st.text_input('Endereço',value=dados['logradouro'],disabled=True).upper()
                col3,col4=st.columns(2)
                temp_dict['cep']=col3.text_input('CEP',value=dados['cep'],disabled=True).upper()
                temp_dict['numero']=col4.text_input('Número',value=dados['numero'],disabled=True).upper()

                col5,col6,col7=st.columns(3)
                temp_dict['bairro']=col5.text_input('Bairro',value=dados['bairro'],disabled=True).upper()
                temp_dict['municipio']=col6.text_input('Cidade',value=dados['municipio'],disabled=True).upper()
                temp_dict['uf']=col7.text_input('UF',value=dados['uf'],disabled=True).upper()
                temp_dict['complemento']=st.text_input('Complemento',value=dados['complemento'],disabled=True).upper()

                temp_dict['email']=st.text_input('E-mail',value=str(dados['email']).upper(),disabled=True).upper()
                temp_dict['telefone']=st.text_input('Telefone',value=dados['telefone'],disabled=True).upper()

                btn=st.button('Enviar',key='btn_send')

                if btn==True:

                    resp=ValidarCampos(temp_dict)

                    if resp[0]!=None:

                        mensagem=st.warning(f'Preencher o campo {resp[0]}')
                        time.sleep(1)
                        mensagem.empty()

                        pass

                    else:

                        path_base=os.path.join(os.getcwd(),temp_dict['cnpj'])
                        os.makedirs(path_base,exist_ok=True)
                        temp_path=os.path.join(path_base,'Cadastro.xlsx')

                        df=pd.DataFrame(columns=temp_dict.keys())
                        df.loc[len(df)]=temp_dict.values()

                        colunas=df.columns[1:].tolist()
                        df=df[colunas]

                        df.to_excel(temp_path,index=False)

                        msg='Bom dia' if datetime.now().hour<12 else 'Boa tarde'

                        assunto=f'Cadastro {temp_dict["fantasia"]}'

                        mensagem=f"""
                        
                        <p>{msg};</p>

                        <p>Segue o e-mail com os dados cadastrais para fazer o pedido.</p>

                        <P>Por favor não responder mensagem automática</P>

                        <p>Atenciosamente</p>

                        <p>BOT TI</p>
                        
                        """

                        anexo=glob(temp_path)
                        email_dict={'To':[temp_dict['consultor']],'CC':['raquel@demarchisaopaulo.com.br'],'Anexo':anexo}
                        mail.Enviar(assunto=assunto,mensagem=mensagem,info=email_dict)

                        mensagem=st.success('E-mail enviado com sucesso')
                        time.sleep(1)
                        mensagem.empty()

                        shutil.rmtree(path_base)
                        time.sleep(2)
                        streamlit_js_eval(js_expressions='parent.window.location.reload()')
                        
                        pass

                    pass

                pass

            pass

        pass

    pass

def ValidarCampos(temp_dict: dict):

    cont=0

    dados_dict=dict()

    for k,v in temp_dict.items():

        if str(v)=='':

            cont=0

            dados_dict[cont]=k

            break

        else:

            cont+=1

            dados_dict[0]=None

            pass

        pass

    return dados_dict

    pass


if __name__=='__main__':

    main()

    pass