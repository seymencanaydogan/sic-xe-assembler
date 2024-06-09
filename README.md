# SIC/XE Assembler
> SIC/XE (Simplified Instructional Computer / Extended Edition), bilgisayar mimarisi ve derleyici tasarımı konusunda eğitim amaçlı kullanılan bir sistemdir. SIC/XE, daha basit bir versiyonu olan SIC (Simplified Instructional Computer) üzerine geliştirilmiş bir sistemdir ve öğrencilere bilgisayar mimarisi, makine dili, montaj dili ve düşük seviyeli programlama konularını öğretmek için tasarlanmıştır. SIC/XE'de bir Assembler, montaj dilinde yazılmış bir programı makine diline çeviren bir programdır. Montaj dili, insanların okuyabileceği semboller ve talimatlarla yazılırken, makine dili doğrudan donanım tarafından çalıştırılabilir. SIC/XE assembler'ı, bu dönüşüm işlemini iki geçişli bir süreçle gerçekleştirir: pass1 ve pass2. İşte bu süreçlerin nasıl çalıştığının kısa bir açıklamasını yapalım:
> 
> Pass 1 (Birinci Geçiş): 
> 
> 1. Başlangıç Adresi ve Program Uzunluğunu Belirleme: Programın başlangıç adresi okunur ve programın toplam uzunluğu hesaplanır.
> 2. Sembol Tablosu Oluşturma: Programdaki her bir sembol (etiket) ve ilgili bellek adresi sembol tablosuna eklenir. Bu tablo, ikinci geçişte kullanılmak üzere oluşturulur.
> 3. Adres Hesaplama: Her talimatın ve verinin bellekteki adresi hesaplanır. Bu adresler, sembol tablosuna ve geçici bir dosyaya kaydedilir.
> 4. Program Blokları Yönetimi: Eğer program blokları (program segmentleri) kullanılıyorsa, her blok için ayrı adresleme yapılır ve blokların başlangıç adresleri kaydedilir.
> 
> Pass 2 (İkinci Geçiş):
> 
> 1. Kod Üretimi: Her talimat ve veri için uygun makine kodu üretilir. Sembol tablosundaki adresler kullanılarak talimatların operantları çözülür.
> 2. Nesne Kodu Üretimi: Makine kodu, nesne dosyası adı verilen bir dosyada saklanır. Bu dosya, programın çalıştırılabilir formunu içerir.
> 3. Hata Kontrolü: Sembollerle ilgili olası hatalar (tanımsız semboller, yanlış adreslemeler vb.) kontrol edilir ve hata raporları oluşturulur.
> 4. Nesne Program ve Yükleme: Üretilen nesne kodu, hedef makinede çalıştırılmak üzere yükleyici (loader) tarafından belleğe yerleştirilir.

## Programın Çalışması
Ana klasöre girdikten sonra, "dist" adlı klasörde bulunan assembler.exe dosyasını çalıştırın. Program, sizden assembly edilecek kodu girmenizi isteyecektir. Bu kodu, ana dizindeki "ornek_programlar" klasöründe bulunan programlardan (örneğin, 2-5 veya 2-15) birini açıp kopyala-yapıştır yöntemiyle bu alana girebilirsiniz. "Assembly et" butonuna bastığınızda, eğer kodda bir hata yoksa program başarıyla obje dosyasını oluşturacak ve ekranda görüntüleyecektir. Hata ile karşılaşmanız durumunda, bir mesaj kutusu ile uyarı alacak ve aynı zamanda komut istemcisi ekranında hata mesajı görüntülenecektir.

## Özellikler

- Talimat Formatları ve Adresleme Modları
	- Doğrudan Adresleme Modu: Bu modda, operandın adresi talimatta doğrudan belirtilir. Bellekteki belirli bir adrese erişmek için kullanılır.
	- Dolaylı Adresleme Modu: Bu modda, talimatta belirtilen adres, operandın bulunduğu bellek adresini gösterir. Yani, önce bu adresin içeriği okunur ve gerçek operandın adresine ulaşılır.
	- Basit Adresleme Modu: Bu modda, operandın adresi talimatta doğrudan belirtilir ve adresleme genellikle kayıtlarla yapılır. Bu mod, diğer adresleme modlarıyla karıştırılmamalıdır.
	- Hemen Adresleme Modu: Bu modda, operand doğrudan talimatta belirtilir ve anında kullanılır. Operandın adresi yerine kendisi talimatta yer alır.
		- Program Sayacı (PC Register): Bu kayıt, yürütülen sonraki talimatın adresini tutar. Adresleme, PC register kullanılarak gerçekleştirilir.
		- Base (Base Register): Bu kayıt, bellekteki belirli bir bölgeyi baz alarak adresleme yapmak için kullanılır. Adresler, base register ile hesaplanır.
	- Genişletilmiş Talimat (4 bit Talimat): SIC/XE'de bazı talimatlar, 4 bayt (32 bit) uzunluğunda olabilir. Bu genişletilmiş talimatlar, daha büyük adres alanlarını destekler ve daha karmaşık işlemler gerçekleştirebilir.
- Program Relocation (Yeniden Konumlandırma)
	- Program Blokları: Program, bellekte ayrı bloklara bölünebilir. Her blok, farklı bir bellek bölgesinde bulunabilir ve bağımsız olarak yerleştirilebilir. Bu, bellek yönetimini optimize eder.
	- Kontrol Bölümleri: Programlar, bağımsız olarak yüklenebilen ve çalıştırılabilen kontrol bölümlerine ayrılabilir. Her kontrol bölümü, kendi başına çalışabilen kod ve veri içerir.
	- Program Bağlantısı
		- Harici Tanımlama: Bir programın başka programlarda kullanılabilecek sembolleri tanımlaması.
		- Harici Referans: Bir programın başka programlarda tanımlanan sembollere başvurması.
		- Modifikasyon Kaydı: Yeniden konumlandırma sırasında programın belirli bölümlerinin nasıl değiştirilmesi gerektiğini belirten kayıt. Adreslerin ve referansların uygun şekilde ayarlanmasını sağlar.
- Diğerleri
	- Literal: Programda sabit değerlere referans vermek için kullanılan semboller. Literaller, genellikle programın belleğinde saklanır ve belirli talimatlarla doğrudan kullanılır. Literaller, derleyici tarafından otomatik olarak belleğe yerleştirilir ve kullanımı optimize edilir.

## Algoritma

- Pass 1
	- Her program bloğu bilgisini kaydet
		- Semboller
		- Literaller
		- Harici Tanımlama
		- Harici Referans
		- Modifikasyon Kaydı
	- Program adresini sayma
- Pass 2
	- Talimat Formatı
	- Makine Kodu Üretme

## SIC/XE için İşlem Tablosu (Optab)

| Anımsatıcı  | Format | Opcode | Efekt                           |Notlar
|-------------|:------:|:------:|---------------------------------|:-----:
| ADD m       |  3/4   |   18   | A ← (A) + (m..m+2)              |
| ADDF m      |  3/4   |   58   | F ← (F) + (m..m+5)              |F
| ADDR r1,r2  |   2    |   90   | r2 ← (r2) + (r1)                
| AND m       |  3/4   |   40   | A ← (A) & (m..m+2)              
| CLEAR r1    |   2    |   B4   | r1 ← 0                          
| COMP m      |  3/4   |   28   | A : (m..m+2)                    |C
| COMPF m     |  3/4   |   88   | F : (m..m+5)                    |CF
| COMPR r1,r2 |   2    |   A0   | (r1) : (r2)                     |C
| DIV m       |  3/4   |   24   | A : (A) / (m..m+2)              
| DIVF m      |  3/4   |   64   | F : (F) / (m..m+5)              |F
| DIVR r1,r2  |   2    |   9C   | (r2) ← (r2) / (r1)              
| FIX         |   1    |   C4   | A ← (F) [convert to integer]    
| FLOAT       |   1    |   C0   | F ← (A) [convert to floating]   |F
| HIO         |   1    |   F4   | Halt I/O channel number (A)     |P
| J m         |  3/4   |   3C   | PC ← m                          
| JEQ m       |  3/4   |   30   | PC ← m if CC set to =           
| JGT m       |  3/4   |   34   | PC ← m if CC set to >           
| JLT m       |  3/4   |   38   | PC ← m if CC set to <           
| JSUB m      |  3/4   |   48   | L ← (PC); PC ← m<               
| LDA m       |  3/4   |   00   | A ← (m..m+2)                    
| LDB m       |  3/4   |   68   | B ← (m..m+2)                    
| LDCH m      |  3/4   |   50   | A [rightmost byte] ← (m)        
| LDF m       |  3/4   |   70   | F ← (m..m+5)                    |F
| LDL m       |  3/4   |   08   | L ← (m..m+2)                    
| LDS m       |  3/4   |   6C   | S ← (m..m+2)                    
| LDT m       |  3/4   |   74   | T ← (m..m+2)                    
| LDX m       |  3/4   |   04   | X ← (m..m+2)                    
| LPS m       |  3/4   |   D0   | Load processor status           |P
| MUL m       |  3/4   |   20   | A ← (A) * (m..m+2)              
| MULF m      |  3/4   |   60   | F ← (F) * (m..m+5)              
| MULR r1,r2  |   2    |   98   | r2 ← (r2) * (r1)                
| NORM        |   1    |   C8   | F ← (F) [normalized]            |F
| OR m        |  3/4   |   44   | A ← (A)  (m..m+2)               
| RD m        |  3/4   |   D8   | A [rightmost byte] ← data       |P
| RMO r1,r2   |   2    |   AC   | r2 ← (r1)                       
| RSUB        |  3/4   |   4C   | PC ← (L)                        
| SHIFTL r1,n |   2    |   A4   | r1 ← (r1); left circular shift  
| SHIFTR r1,n |   2    |   A8   | r1 ← (r1); right shift n bits   
| SIO         |   1    |   F0   | Start I/O channel number (A)    |P
| SSK m       |  3/4   |   EC   | Protection key for address m    |P
| STA m       |  3/4   |   0C   | m..m+2 ← (A)                    
| STB m       |  3/4   |   78   | m..m+2 ← (B)                    
| STCH m      |  3/4   |   54   | m ← (A) [rightmost byte]        
| STF m       |  3/4   |   80   | m..m+5 ← (F)                    |F
| STI m       |  3/4   |   D4   | Interval timer value ← (m..m+2) |P
| STL m       |  3/4   |   14   | m..m+2 ← (L)                    
| STS m       |  3/4   |   7C   | m..m+2 ← (S)                    
| STSW m      |  3/4   |   E8   | m..m+2 ← (SW)                   |P
| STT m       |  3/4   |   84   | m..m+2 ← (T)                    
| STX m       |  3/4   |   10   | m..m+2 ← (X)                    
| SUB m       |  3/4   |   1C   | A ← (A) - (m..m+2)              
| SUBF m      |  3/4   |   5C   | F ← (F) - (m..m+5)              |F
| SUBR r1,r2  |   2    |   94   | r2 ← (r2) - (r1)                
| SVC n       |   2    |   B0   | Generate SVC interrupt          
| TD m        |  3/4   |   E0   | Test device specified by (m)    |PC
| TIO         |   1    |   F8   | Test I/O channel number (A)     |PC
| TIX m       |  3/4   |   2C   | X ← (X) + 1; (X) : (m..m+2)     |C
| TIXR r1     |   2    |   B8   | X ← (X) + 1; (X) : (r1)         |C
| WD m        |  3/4   |   DC   | Device specified by (m) ← (A)   |P

### Örnek 1 (2-5.asm)

```sic/xe
COPY 	START 	0 		 
FIRST 	STL 	RETADR 		 	 
		LDB    #LENGTH	 	 	 
		BASE 	LENGTH 		 	 	 
ENDFIL 	LDA 	EOF 		 	 
		STA 	BUFFER 		 
		LDA    #3 		 	 
		STA 	LENGTH 		 
       +JSUB 	WRREC 		 	 
		J      @RETADR 		 	 
EOF 	BYTE 	C'EOF' 		 
RETADR  RESW 	1 		 
LENGTH 	RESW 	1
BUFFER 	RESB 4096		 	 
	.			 
	.	SUBROUTINE TO READ RECORD INTO BUFFER 	 
	.				 
RDREC 	CLEAR 	X
		CLEAR 	A 		 	 
		CLEAR 	S 		 	 
       +LDT     #4096 		 
RLOOP 	TD 	    INPUT 		 	 
		JEQ 	RLOOP 		 	 
		RD 		INPUT 		 	 
		COMPR 	A,S 		 	 
		JEQ 	EXIT 		 	 
		STCH 	BUFFER,X 	 	 
		TIXR 	T 		 	 
		JLT 	RLOOP 		 	 
EXIT 	STX 	LENGTH 		 	 
		RSUB 			 	 
INPUT 	BYTE 	X'F1' 		 	 
	.		 
	.	SUBROUTINE TO WRITE RECORD FROM BUFFER 	 
	.		 
WRREC 	CLEAR 	X 		 	 
		LDT 	LENGTH 		 
WLOOP 	TD 		OUTPUT 		 	 
		JEQ 	WLOOP 		 	 
		LDCH 	BUFFER,X 	 	 
		WD 		OUTPUT 		 	 
		TIXR 	T 		 	 
		JLT 	WLOOP 		 	 
		RSUB 			 	 
OUTPUT 	BYTE 	X'05' 		 	 
		END 	FIRST 	
```
### Çıktı (Obje Program) (2-5.asm)

```txt
HCOPY  000000001063
T0000001E1720196920190320100F20160100030F200D4B1010493E2003454F46B410
T0010241EB400B44075101000E32019332FFADB2013A00433200857C003B8503B2FEA
T0010421D1340004F0000F1B410774000E32011332FFA53C003DF2008B8503B2FEF
T00105F044F000005
E000000
```
### Örnek 2 (2-15.asm)

```sic/xe
COPY    START	0
	    EXTDEF  BUFFER,BUFEND,LENGTH
	    EXTREF  RDREC,WRREC
FIRST   STL     RETADR		
CLOOP  +JSUB	RDREC		
		LDA		LENGTH		
		COMP   #0		
		JEQ		ENDFIL
       +JSUB	WRREC		
		J		CLOOP		
ENDFIL	LDA    =C'EOF'		
		STA		BUFFER		
		LDA    #3		
		STA		LENGTH		
       +JSUB	WRREC		
		J      @RETADR		
RETADR	RESW	1
LENGTH	RESW	1
		LTORG		
BUFFER	RESB	4096
BUFEND	EQU		*
MAXLEN	EQU		BUFEND-BUFFER

RDREC	CSECT
.
.		SUBROUTTINE TO READ RECORD INTO BUFFER
.
		EXTREF	BUFFER,LENGTH,BUFEND
		CLEAR	X		
		CLEAR	A		
		CLEAR	S		
		LDT		MAXLEN		
RLOOP	TD		INPUT		
		JEQ		RLOOP		
		RD		INPUT		
		COMPR	A,S		
		JEQ		EXIT		
       +STCH	BUFFER,X	
		TIXR	T		
		JLT		RLOOP		
EXIT   +STX		LENGTH		
		RSUB			
INPUT	BYTE	X'F1'		
MAXLEN	WORD	BUFEND-BUFFER	

WRREC	CSECT
.
.		SUBROUTINE TO WRITE RECORD FROM BUFFER
.
		EXTREF	LENGTH,BUFFER
		CLEAR	X		
       +LDT		LENGTH		
WLOOP	TD     =X'05'		
		JEQ		WLOOP		
	   +LDCH	BUFFER,X	
		WD     =X'05'		
		TIXR	T		
		JLT		WLOOP		
		RSUB			
		END		FIRST
```

### Çıktı (Obje Program) (2-15.asm)

```txt
HCOPY  000000001033
DBUFFER000033BUFEND001033LENGTH00002D
RRDREC WRREC
T0000001D1720274B1000000320232900003320074B1000003F2FEC0320160F2016
T00001D100100030F200A4B1000003E2000454F46
M00000405+RDREC
M00001105+WRREC
M00002405+WRREC
E000000

HRDREC 00000000002B
RBUFFERLENGTHBUFEND
T0000001DB410B400B44077201FE3201B332FFADB2015A00433200957900000B850
T00001D0E3B2FE9131000004F0000F1000000
M00001805+BUFFER
M00002105+LENGTH
M00002806+BUFEND
M00002806-BUFFER
E

HWRREC 00000000001C
RLENGTHBUFFER
T0000001BB41077100000E32012332FFA53900000DF2008B8503B2FEE4F0000
M00000305+LENGTH
M00000D05+BUFFER
E
```

### Proje/Tasarım'ı Hazırlayan
B210109063 Seymen Can Aydoğan