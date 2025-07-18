import re
from datetime import datetime

entrada = """
Debito	24/04/2023	Transferência - Liquidação	XPLG11 - XP LOG FUNDO DE INVESTIMENTO IMOBILIARIO FII	NU INVEST CORRETORA DE VALORES S.A.	8	-R$ 96,96-
Debito	25/01/2023	Transferência - Liquidação	BBPO11 - BB PROGRESSIVO II FII - FII	NU INVEST CORRETORA DE VALORES S.A.	3	-R$ 86,03-
Debito	25/01/2023	Transferência - Liquidação	HFOF11 - HEDGE TOP FOFII 3 FDO INV IMOB	NU INVEST CORRETORA DE VALORES S.A.	12	-R$ 67,808-
Debito	25/01/2023	Transferência - Liquidação	MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII	NU INVEST CORRETORA DE VALORES S.A.	2	-R$ 10,07-
Debito	25/01/2023	Transferência - Liquidação	RBVA11 - FDO INV IMOB RIO BRAVO RENDA VAREJO - FII	NU INVEST CORRETORA DE VALORES S.A.	3	-R$ 94,48-
Debito	25/01/2023	Transferência - Liquidação	VILG11 - FII VINCI LG	NU INVEST CORRETORA DE VALORES S.A.	3	-R$ 95,56-
Debito	24/01/2023	Transferência - Liquidação	KISU11 - KILIMA FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS IMOBILIÁRIOS	NU INVEST CORRETORA DE VALORES S.A.	61	-R$ 8,08-
Debito	24/01/2023	Transferência - Liquidação	RBRP11 - FII RBR PROP	NU INVEST CORRETORA DE VALORES S.A.	5	-R$ 47,968-
Debito	24/01/2023	Transferência - Liquidação	RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE	NU INVEST CORRETORA DE VALORES S.A.	35	-R$ 52,355-
Debito	24/01/2023	Transferência - Liquidação	XPSF11 - XP SELECTION FUNDO DE FIM - FII	NU INVEST CORRETORA DE VALORES S.A.	103	-R$ 7,40-
"""

entrada2 = """Credito        04/11/2022        Transferência - Liquidação        ARCT11 - RIZA ARCTIUM REAL ESTATE FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 99,33 
Credito        29/09/2022        Transferência - Liquidação        ARCT11 - RIZA ARCTIUM REAL ESTATE FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 100,20 
Credito        29/07/2022        Transferência - Liquidação        BBPO11 - BB PROGRESSIVO II FII - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 78,54 
Credito        18/10/2022        Transferência - Liquidação        BBRC11 - BB RENDA CORPORATIVA FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 100,00 
Credito        04/10/2022        Transferência - Liquidação        BBRC11 - BB RENDA CORPORATIVA FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 101,93 
Credito        16/08/2022        Transferência - Liquidação        BIME11 - BRIO MULTIESTRATEGIA - FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        20         R$ 9,27 
Credito        15/08/2022        Transferência - Liquidação        BIME11 - BRIO MULTIESTRATEGIA - FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 9,33 
Credito        11/08/2022        Transferência - Liquidação        BIME11 - BRIO MULTIESTRATEGIA - FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        17         R$ 9,26 
Credito        03/08/2022        Transferência - Liquidação        BIME11 - BRIO MULTIESTRATEGIA - FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,41 
Credito        22/07/2022        Transferência - Liquidação        BIME11 - BRIO MULTIESTRATEGIA - FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,45 
Credito        19/12/2022        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 57,84 
Credito        25/11/2022        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 59,58 
Credito        18/11/2022        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 62,40 
Credito        29/08/2022        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 66,05 
Credito        29/07/2022        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 55,06 
Credito        15/08/2022        Transferência - Liquidação        DEVA11 - FII DEVANT          NU INVEST CORRETORA DE VALORES S.A.        4         R$ 92,798 
Credito        11/08/2022        Transferência - Liquidação        DEVA11 - FII DEVANT          NU INVEST CORRETORA DE VALORES S.A.        1         R$ 96,35 
Credito        22/07/2022        Transferência - Liquidação        DEVA11 - FII DEVANT          NU INVEST CORRETORA DE VALORES S.A.        1         R$ 98,91 
Credito        22/07/2022        Transferência - Liquidação        GAME11 - FUNDO DE INVESTIMENTO IMOBILIARIO GUARDIAN MULTIESTRATEGIA IMOBILIARIA I        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,90 
Credito        29/08/2022        Transferência - Liquidação        GGRC11 - GGR COVEPI RENDA FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 114,20 
Credito        25/11/2022        Transferência - Liquidação        HCTR11 - HECTARE CE - FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 98,85 
Credito        04/11/2022        Transferência - Liquidação        HCTR11 - HECTARE CE - FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 102,685 
Credito        29/09/2022        Transferência - Liquidação        HCTR11 - HECTARE CE - FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 103,04 
Credito        22/07/2022        Transferência - Liquidação        JPPA11 - JPP CAPITAL RECEBIVEIS IMOB. FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 101,29 
Credito        26/08/2022        Transferência - Liquidação        KISU11 - KILIMA FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS IMOBILIÁRIOS        NU INVEST CORRETORA DE VALORES S.A.        20         R$ 8,03 
Credito        24/08/2022        Transferência - Liquidação        KISU11 - KILIMA FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS IMOBILIÁRIOS        NU INVEST CORRETORA DE VALORES S.A.        24         R$ 8,05 
Credito        21/07/2022        Transferência - Liquidação        KISU11 - KILIMA FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS IMOBILIÁRIOS        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 7,64 
Credito        21/07/2022        Transferência - Liquidação        MCHF11 - MAUA CAPITAL HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,21 
Credito        22/12/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 9,89 
Credito        19/12/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        22         R$ 9,83 
Credito        29/11/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        11         R$ 10,04 
Credito        25/11/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 10,05 
Credito        23/11/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        38         R$ 10,10 
Credito        11/11/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 10,25 
Credito        10/11/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 10,26 
Credito        28/10/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 10,25 
Credito        26/10/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 10,25 
Credito        18/10/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 10,29 
Credito        30/09/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 10,27 
Credito        24/08/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        43         R$ 10,02 
Credito        03/08/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 9,78 
Credito        21/07/2022        Transferência - Liquidação        MXRF11 - MAXI RENDA FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,74 
Credito        29/12/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 42,93 
Credito        11/11/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 46,82 
Credito        21/09/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 46,586 
Credito        15/09/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 46,79 
Credito        29/08/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 46,58 
Credito        26/08/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 46,46 
Credito        25/08/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 46,47 
Credito        11/08/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 45,53 
Credito        29/07/2022        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 45,45 
Credito        07/11/2022        Transferência - Liquidação        RBRP11 - FII RBR PROP        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 55,28 
Credito        29/07/2022        Transferência - Liquidação        RBRP11 - FII RBR PROP        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 51,08 
Credito        29/07/2022        Transferência - Liquidação        RBVA11 - FDO INV IMOB RIO BRAVO RENDA VAREJO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 89,67 
Credito        07/11/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 59,25 
Credito        01/11/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 59,48 
Credito        25/10/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 60,03 
Credito        19/10/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 59,96 
Credito        30/09/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 61,64 
Credito        29/09/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 61,99 
Credito        15/09/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 61,65 
Credito        29/08/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 63,24 
Credito        29/07/2022        Transferência - Liquidação        RECT11 - FUNDO DE INVESTIMENTO IMOBILIARIO - FII UBS (BR) OFFICE        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 57,00 
Credito        21/07/2022        Transferência - Liquidação        RZAG11 - O FUNDO DE INVESTIMENTO NAS CADEIAS PRODUTIVAS AGROINDUSTRIAIS RIZA AGRO FIAGRO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 10,19 
Credito        22/08/2022        Transferência - Liquidação        TORD11 - TORDESILHAS EI FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 8,03 
Credito        17/08/2022        Transferência - Liquidação        TORD11 - TORDESILHAS EI FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 8,29 
Credito        15/08/2022        Transferência - Liquidação        TORD11 - TORDESILHAS EI FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        29         R$ 8,081 
Credito        11/08/2022        Transferência - Liquidação        TORD11 - TORDESILHAS EI FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        25         R$ 8,45 
Credito        21/07/2022        Transferência - Liquidação        TORD11 - TORDESILHAS EI FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 8,67 
Credito        22/07/2022        Transferência - Liquidação        VCRI11 - VINCI CREDIT SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 9,31 
Credito        21/07/2022        Transferência - Liquidação        VCRI11 - VINCI CREDIT SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,31 
Credito        05/12/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        11         R$ 9,05 
Credito        01/12/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        11         R$ 9,03 
Credito        11/11/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        19         R$ 9,32 
Credito        04/11/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 9,38 
Credito        18/10/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        22         R$ 9,35 
Credito        21/09/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 9,87 
Credito        20/09/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 9,86 
Credito        16/09/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        12         R$ 9,83 
Credito        15/09/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 9,88 
Credito        22/08/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 9,802 
Credito        16/08/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        24         R$ 9,79 
Credito        11/08/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        11         R$ 9,765 
Credito        03/08/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        15         R$ 9,78 
Credito        21/07/2022        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 9,88 
Credito        21/07/2022        Transferência - Liquidação        VGIA11 - VALORA CRA FUNDO DE INVESTIMENTO NAS CADEIAS PRODUTIVAS AGROINDUSTRIAIS - FIAGRO-IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 10,16 
Credito        15/08/2022        Transferência - Liquidação        VGIP11 - VALORA CRI ÍNDICE DE PREÇO FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 91,355 
Credito        22/07/2022        Transferência - Liquidação        VGIP11 - VALORA CRI ÍNDICE DE PREÇO FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 96,16 
Credito        29/07/2022        Transferência - Liquidação        VILG11 - FII VINCI LG        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 92,813 
Credito        21/07/2022        Transferência - Liquidação        VIUR11 - VINCI IMOVEIS URBANOS FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 6,941 
Credito        21/07/2022        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,20 
Credito        22/07/2022        Transferência - Liquidação        XPCA11 - XP CRÉDITO AGRÍCOLA FDO INV FIAGRO IMOBILIÁRIO        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 10,30 
Credito        23/12/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 7,14 
Credito        19/12/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        15         R$ 7,08 
Credito        12/12/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 7,23 
Credito        05/12/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 7,23 
Credito        29/08/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 7,57 
Credito        26/08/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        19         R$ 7,58 
Credito        11/08/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        12         R$ 7,01 
Credito        03/08/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        16         R$ 7,058 
Credito        21/07/2022        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 7,01 
Credito        13/12/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,24 
Credito        05/12/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 9,23 
Credito        14/11/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 9,31 
Credito        23/08/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 3,88 
Credito        16/08/2023        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUEIS FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 58,00 
Credito        16/08/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 3,99 
Credito        10/08/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        12         R$ 3,93 
Credito        03/08/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 9,45 
Credito        31/07/2023        Transferência - Liquidação        RZAT11 - RIZA ARCTIUM REAL ESTATE FUNDO DE INVESTIMENTO IMOBILIARIO        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 90,67 
Credito        31/07/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 9,56 
Credito        31/07/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 4,29 
Credito        19/07/2023        Transferência - Liquidação        BLMG11 - BLUEMACAW LOGÍSTICA FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 68,29 
Credito        19/07/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 4,67 
Credito        17/07/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 4,76 
Credito        10/07/2023        Transferência - Liquidação        BLMG11 - BLUEMACAW LOGÍSTICA FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 68,00 
Credito        19/06/2023        Transferência - Liquidação        BLMG11 - BLUEMACAW LOGÍSTICA FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 67,99 
Credito        19/06/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        7         R$ 9,27 
Credito        05/06/2023        Transferência - Liquidação        BLMG11 - BLUEMACAW LOGÍSTICA FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 66,72 
Credito        05/06/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 9,29 
Credito        05/06/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 5,41 
Credito        27/04/2023        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 42,45 
Credito        24/04/2023        Transferência - Liquidação        MFII11 - MÉRITO DESENVOLVIMENTO IMOBILIÁRIO I FII - FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 88,68 
Credito        24/04/2023        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUEIS FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 56,35 
Credito        24/04/2023        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        50         R$ 6,92 
Credito        12/04/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 8,79 
Credito        05/04/2023        Transferência - Liquidação        BCFF11 - FDO INV IMOB - FII BTG PACTUAL FUNDO DE FUNDOS        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 62,28 
Credito        24/03/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 6,95 
Credito        20/03/2023        Transferência - Liquidação        QAGR11 - QUASAR AGRO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 41,19 
Credito        20/03/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 9,07 
Credito        20/03/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 7,12 
Credito        15/03/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 9,05 
Credito        15/03/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 6,97 
Credito        27/02/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 9,09 
Credito        16/02/2023        Transferência - Liquidação        BRCR11 - FDO INV IMOB - FII BTG PACTUAL CORPORATE OFFICE FUND        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 54,33 
Credito        16/02/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 9,00 
Credito        13/02/2023        Transferência - Liquidação        BBRC11 - BB RENDA CORPORATIVA FII        NU INVEST CORRETORA DE VALORES S.A.        1         R$ 92,92 
Credito        13/02/2023        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUEIS FII        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 56,83 
Credito        13/02/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        15         R$ 9,02 
Credito        06/02/2023        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        14         R$ 9,01 
Credito        25/01/2023        Transferência - Liquidação        BLMG11 - BLUEMACAW LOGÍSTICA FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        3         R$ 71,69 
Credito        25/01/2023        Transferência - Liquidação        KNCR11 - KINEA RENDIMENTOS IMOBILIARIOS FUNDO DE INVESTIMENTO IMOBILI        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 98,42 
Credito        25/01/2023        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        100         R$ 8,74 
Credito        25/01/2023        Transferência - Liquidação        XPLG11 - XP LOG FUNDO DE INVESTIMENTO IMOBILIARIO FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 91,884 
Credito        24/01/2023        Transferência - Liquidação        BCFF11 - FDO INV IMOB - FII BTG PACTUAL FUNDO DE FUNDOS        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 64,924 
Credito        24/01/2023        Transferência - Liquidação        HCTR11 - HECTARE CE - FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        6         R$ 98,97 
Credito        24/01/2023        Transferência - Liquidação        HFOF11 - HEDGE TOP FOFII 3 FDO INV IMOB        NU INVEST CORRETORA DE VALORES S.A.        12         R$ 67,70 
Credito        24/01/2023        Transferência - Liquidação        MFII11 - MÉRITO DESENVOLVIMENTO IMOBILIÁRIO I FII - FII        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 95,49 
Credito        24/01/2023        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUEIS FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 62,298 
Credito        17/01/2023        Transferência - Liquidação        KISU11 - KILIMA FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS IMOBILIÁRIOS        NU INVEST CORRETORA DE VALORES S.A.        11         R$ 7,95 
Credito        13/01/2023        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 7,18 
Credito        10/01/2023        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        13         R$ 7,20 
Credito        31/10/2024        Transferência - Liquidação        MXRF11 - MAXI RENDA FDO INV IMOB - FII        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 9,60 
Credito        16/10/2024        Transferência - Liquidação        MXRF11 - MAXI RENDA FDO INV IMOB - FII        NU INVEST CORRETORA DE VALORES S.A.        9         R$ 9,79 
Credito        05/09/2024        Transferência - Liquidação        MXRF11 - MAXI RENDA FDO INV IMOB - FII        NU INVEST CORRETORA DE VALORES S.A.        15         R$ 10,01 
Credito        18/06/2024        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUÉIS FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        2         R$ 46,00 
Credito        18/06/2024        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 8,82 
Credito        04/04/2024        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        4         R$ 9,09 
Credito        25/06/2025        Transferência - Liquidação        XPSF11 - XP SELECTION FUNDO DE FIM - FII        NU INVEST CORRETORA DE VALORES S.A.        15         R$ 6,10 
Credito        23/06/2025        Transferência - Liquidação        MXRF11 - MAXI RENDA FDO INV IMOB - FII        NU INVEST CORRETORA DE VALORES S.A.        10         R$ 9,36 
Credito        11/06/2025        Transferência - Liquidação        MXRF11 - MAXI RENDA FDO INV IMOB - FII        NU INVEST CORRETORA DE VALORES S.A.        20         R$ 9,40 
Credito        11/06/2025        Transferência - Liquidação        SARE11 - SANTANDER RENDA DE ALUGUÉIS FDO. INVEST. IMOB.        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 4,73 
Credito        11/06/2025        Transferência - Liquidação        VSLH11 - VERSALHES RECEBÍVEIS IMOBILIÁRIOS - FDO. INV. IMOB        NU INVEST CORRETORA DE VALORES S.A.        8         R$ 2,94 
Credito        10/06/2025        Transferência - Liquidação        VGHF11 - VALORA HEDGE FUND FUNDO DE INVESTIMENTO IMOBILIARIO - FII        NU INVEST CORRETORA DE VALORES S.A.        5         R$ 7,63"""
linhas = entrada.splitlines()

for linha in linhas:
    if "Transferência" in linha and "Debito" in linha:
        try:
            partes = linha.split("\t")

            data_br = partes[1].strip()
            data_iso = datetime.strptime(data_br, "%d/%m/%Y").strftime("%Y-%m-%d")

            descricao = partes[3].strip()
            codigo = re.search(r'([A-Z]{4}\d{2})', descricao)
            if not codigo:
                continue
            codigo = codigo.group(1)

            quantidade = partes[5].strip().replace('.', '').replace(',', '.')
            preco = partes[6].strip().replace('R$', '').replace('.', '').replace(',', '.')

            print(f"python fiiprovisor.py add_venda {codigo} {data_iso} {quantidade} {preco}")
        except Exception as e:
            continue  # Ignora qualquer linha que não esteja bem formatada
