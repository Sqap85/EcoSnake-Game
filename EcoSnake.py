#!/usr/bin/env python3
"""
EcoSnake Game - Çevre Koruma Temalı Yılan Oyunu
Copyright (c) 2025 Sqap85

Bu proje MIT lisansı altında yayınlanmıştır.
Detaylar için LICENSE dosyasına bakınız.
"""

import pygame
import os
import random
import sys
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Pygame'i başlat
pygame.init()

# Renk Paleti
SIYAH = (20, 20, 30)           # Yumuşak koyu renk
BEYAZ = (250, 250, 255)        # Göz yormayan beyaz
YESIL = (46, 204, 113)         # Modern yeşil (emerald)
KIRMIZI = (231, 76, 60)        # Modern kırmızı 
MAVI = (52, 152, 219)          # Modern mavi
KAHVERENGI = (160, 116, 85)    # Sıcak kahverengi
SARI = (241, 196, 15)          # Altın sarısı
GRI = (149, 165, 166)          # Yumuşak gri
NEON_YESIL = (39, 174, 96)     # Parlak yeşil
MOR = (155, 89, 182)           # Modern mor
TURUNCU = (230, 126, 34)       # Sıcak turuncu
CYAN = (26, 188, 156)          # Modern cyan
KOYU_GRI = (52, 73, 94)        # Koyu gri
ACIK_GRI = (200, 210, 215)     # Daha okunabilir açık gri
CYAN = (0, 255, 255)

# Oyun ayarları
PENCERE_GENISLIK = 800
PENCERE_YUKSEKLIK = 600
KARE_BOYUT = 30

# Hız/zorluk seçenekleri (oyun hızı, düşük = daha yavaş hareket)
HIZLAR = {
    'Kolay': 4,    # Daha yavaş hareket (saniyede 4 hareket)
    'Orta': 8,     # Normal hareket hızı (saniyede 8 hareket)  
    'Zor': 12      # Hızlı hareket (saniyede 12 hareket)
}
FPS = 60  # Ekran yenileme hızı (akıcılık için yüksek tutulmalı)

# Ekranı oluştur
ekran = pygame.display.set_mode((PENCERE_GENISLIK, PENCERE_YUKSEKLIK))
pygame.display.set_caption("EcoSnake-Game")
saat = pygame.time.Clock()


# Görselleri yükle (assets klasöründen)
insan_sprite = pygame.image.load("assets/gardener.png")
insan_sprite = pygame.transform.scale(insan_sprite, (KARE_BOYUT, KARE_BOYUT))
hakantema_sprite = pygame.image.load("assets/hakantema.png")
hakantema_sprite = pygame.transform.scale(hakantema_sprite, (KARE_BOYUT, KARE_BOYUT))
obesity_sprite = pygame.image.load("assets/obesity.png")
obesity_sprite = pygame.transform.scale(obesity_sprite, (KARE_BOYUT, KARE_BOYUT))

# Karakterler sözlüğü
KARAKTERLER = {
    'Bahçıvan': insan_sprite,
    'HakanTema': hakantema_sprite,
    'Tombik Çocuk': obesity_sprite
}

# Çeşitli çöp türleri için sprite'lar
apple_sprite = pygame.image.load("assets/apple.png")
apple_sprite = pygame.transform.scale(apple_sprite, (KARE_BOYUT, KARE_BOYUT))
banana_sprite = pygame.image.load("assets/banana.png")
banana_sprite = pygame.transform.scale(banana_sprite, (KARE_BOYUT, KARE_BOYUT))
bottle_sprite = pygame.image.load("assets/bottle.png")
bottle_sprite = pygame.transform.scale(bottle_sprite, (KARE_BOYUT, KARE_BOYUT))
landfill_sprite = pygame.image.load("assets/landfill.png")
landfill_sprite = pygame.transform.scale(landfill_sprite, (KARE_BOYUT, KARE_BOYUT))

# Taşınan çöp poşeti türleri (kullanıcı seçebilir)
garbage1_sprite = pygame.image.load("assets/garbage1.png") 
garbage1_sprite = pygame.transform.scale(garbage1_sprite, (KARE_BOYUT, KARE_BOYUT))
garbage2_sprite = pygame.image.load("assets/garbage2.png")
garbage2_sprite = pygame.transform.scale(garbage2_sprite, (KARE_BOYUT, KARE_BOYUT))
garbage3_sprite = pygame.image.load("assets/garbage3.png")
garbage3_sprite = pygame.transform.scale(garbage3_sprite, (KARE_BOYUT, KARE_BOYUT))

# Taşınan çöp türleri sözlüğü
GARBAGE_TURLERI = {
    'Tatlı Poşet': garbage1_sprite,
    'Sarı Poşet': garbage2_sprite,
    'Siyah Poşet': garbage3_sprite
}

# Arkaplan görseli
orman_arkaplan = pygame.image.load("assets/orman.png")
orman_arkaplan = pygame.transform.scale(orman_arkaplan, (PENCERE_GENISLIK, PENCERE_YUKSEKLIK))

# Font oluştur
font = pygame.font.Font(None, 36)
buyuk_font = pygame.font.Font(None, 48)
kucuk_font = pygame.font.Font(None, 24)

# Oyuncu verileri
oyuncu_adi = ""
secili_karakter = "Bahçıvan"
secili_arkaplan = "Siyah"
secili_garbage = "Tatlı Poşet"

class CopToplayici:
    def __init__(self, karakter_sprite):
        self.yon_x = 1
        self.yon_y = 0
        self.kareler = []  # [(x, y), ...] ilk eleman baş (karakter), diğerleri poşet
        self.karakter_sprite = karakter_sprite
        # Grid tabanlı başlangıç pozisyonu
        baslangic_x = (PENCERE_GENISLIK // 2 // KARE_BOYUT) * KARE_BOYUT
        baslangic_y = (PENCERE_YUKSEKLIK // 2 // KARE_BOYUT) * KARE_BOYUT
        self.kareler.append((baslangic_x, baslangic_y))

    def hareket_et(self):
        # Yeni baş pozisyonu
        bas_x, bas_y = self.kareler[0]
        yeni_x = bas_x + self.yon_x * KARE_BOYUT
        yeni_y = bas_y + self.yon_y * KARE_BOYUT
        
        # Oyun alanı sınırları (UI alanı hariç)
        UI_ALAN_YUKSEKLIK = 45  # Koyu gri UI alanının yüksekliği
        
        # X ekseni sınırları (sol-sağ duvarlardan sek)
        if yeni_x < 0:
            yeni_x = PENCERE_GENISLIK - KARE_BOYUT
        elif yeni_x >= PENCERE_GENISLIK:
            yeni_x = 0
            
        # Y ekseni sınırları (UI alanının altından başla, alt duvardan sek)
        if yeni_y < UI_ALAN_YUKSEKLIK:
            yeni_y = PENCERE_YUKSEKLIK - KARE_BOYUT
        elif yeni_y >= PENCERE_YUKSEKLIK:
            yeni_y = UI_ALAN_YUKSEKLIK
            
        yeni_bas = (yeni_x, yeni_y)
        # Gövdeyi kaydır
        self.kareler = [yeni_bas] + self.kareler[:-1]

    def cop_topla(self):
        # Son poşet karesinin arkasına yeni bir kare ekle
        self.kareler.append(self.kareler[-1])

    def ciz(self, ekran):
        # Baş (seçili karakter): sprite ile çiz
        bas_x, bas_y = self.kareler[0]
        ekran.blit(self.karakter_sprite, (bas_x, bas_y))
        # Gövde (seçili garbage türü): sprite ile çiz
        secili_garbage_sprite = GARBAGE_TURLERI[secili_garbage]
        for (x, y) in self.kareler[1:]:
            ekran.blit(secili_garbage_sprite, (x, y))

    def carpisma_kontrolu(self):
        # Baş gövdeye çarptı mı?
        bas = self.kareler[0]
        return bas in self.kareler[1:]

class Cop:
    def __init__(self):
        # UI yazılarının olduğu alanları hariç tut (üst 45 piksel)
        # Ayrıca kenar alanları da hariç tut (ulaşılabilir olmayan yerler)
        min_x = 1  # Sol kenarda 1 kare boşluk
        max_x = (PENCERE_GENISLIK // KARE_BOYUT) - 2  # Sağ kenarda 1 kare boşluk
        min_y = 3  # UI alanından sonra
        max_y = (PENCERE_YUKSEKLIK // KARE_BOYUT) - 2  # Alt kenarda 1 kare boşluk
        
        self.x = random.randint(min_x, max_x) * KARE_BOYUT
        self.y = random.randint(min_y, max_y) * KARE_BOYUT
        
        # Rastgele çöp türü seç
        cop_turleri = ['apple', 'banana', 'bottle', 'landfill']
        self.tur = random.choice(cop_turleri)
        
        # Her tür için uygun sprite'ı seç
        if self.tur == 'apple':
            self.sprite = apple_sprite
        elif self.tur == 'banana':
            self.sprite = banana_sprite
        elif self.tur == 'bottle':
            self.sprite = bottle_sprite
        else:  # landfill
            self.sprite = landfill_sprite
    
    def ciz(self, ekran):
        ekran.blit(self.sprite, (self.x, self.y))

# Skor tablosu fonksiyonları
def skor_kaydet(isim, skor, karakter, zorluk):
    try:
        with open('highscores.json', 'r') as f:
            skorlar = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        skorlar = []
    
    yeni_skor = {
        'isim': isim,
        'skor': skor,
        'zorluk': zorluk
    }
    
    skorlar.append(yeni_skor)
    skorlar.sort(key=lambda x: x['skor'], reverse=True)
    skorlar = skorlar[:10]  # En iyi 10 skoru tut
    
    with open('highscores.json', 'w') as f:
        json.dump(skorlar, f, indent=2)

def skor_tablosu_goster():
    try:
        with open('highscores.json', 'r') as f:
            skorlar = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        skorlar = []
    
    while True:
        ekran.fill(SIYAH)
        baslik = buyuk_font.render('SKOR TABLOSU', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        
        if not skorlar:
            mesaj = font.render('Henüz hiç skor kaydedilmemiş!', True, BEYAZ)
            mesaj_rect = mesaj.get_rect(center=(PENCERE_GENISLIK//2, 200))
            ekran.blit(mesaj, mesaj_rect)
        else:
            # Başlıklar - sabit pozisyonlarda
            y_pos = 130
            
            # Sabit pozisyonlar tanımla
            sira_x = 150
            isim_x = 200  
            skor_x = 400
            zorluk_x = 500
            
            # Başlık metinlerini yerleştir
            sira_baslik = kucuk_font.render('No.', True, BEYAZ)
            ekran.blit(sira_baslik, (sira_x, y_pos))
            
            isim_baslik = kucuk_font.render('İsim', True, BEYAZ)
            ekran.blit(isim_baslik, (isim_x, y_pos))
            
            skor_baslik = kucuk_font.render('Skor', True, BEYAZ)
            ekran.blit(skor_baslik, (skor_x, y_pos))
            
            zorluk_baslik = kucuk_font.render('Zorluk', True, BEYAZ)
            ekran.blit(zorluk_baslik, (zorluk_x, y_pos))
            
            y_pos += 25
            
            # Çizgi
            pygame.draw.line(ekran, BEYAZ, (sira_x, y_pos), (zorluk_x + 80, y_pos), 1)
            y_pos += 15
            
            # Skorlar - gradient renk şeması
            for i, skor_bilgi in enumerate(skorlar[:10]):
                if i == 0:  # Altın madalya
                    renk = SARI
                elif i == 1:  # Gümüş madalya  
                    renk = ACIK_GRI
                elif i == 2:  # Bronz madalya
                    renk = TURUNCU
                elif i < 5:  # Top 5
                    renk = CYAN
                else:  # Diğerleri
                    renk = GRI
                
                # Her bilgiyi başlık pozisyonlarına hizala
                sira_text = kucuk_font.render(f"{i+1}.", True, renk)
                ekran.blit(sira_text, (sira_x, y_pos))
                
                isim_text = kucuk_font.render(skor_bilgi['isim'][:12], True, renk)
                ekran.blit(isim_text, (isim_x, y_pos))
                
                skor_text = kucuk_font.render(str(skor_bilgi['skor']), True, renk)
                ekran.blit(skor_text, (skor_x, y_pos))
                
                zorluk_text = kucuk_font.render(skor_bilgi['zorluk'], True, renk)
                ekran.blit(zorluk_text, (zorluk_x, y_pos))
                
                y_pos += 25
        
        # Geri dön bilgisi
        geri = font.render("Geri dönmek için ESC'ye basın", True, GRI)
        geri_rect = geri.get_rect(center=(PENCERE_GENISLIK//2, 520))
        ekran.blit(geri, geri_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE or olay.key == pygame.K_RETURN:
                    return

def isim_gir():
    global oyuncu_adi
    giris = ""
    while True:
        ekran.fill(SIYAH)
        
        # Başlık
        baslik = buyuk_font.render('OYUNCU ADI GİR', True, SARI)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 150))
        ekran.blit(baslik, baslik_rect)
        
        # Giriş kutusu - büyük ve merkezi
        kutu_rect = pygame.Rect(PENCERE_GENISLIK//2 - 200, 220, 400, 60)
        pygame.draw.rect(ekran, (30, 30, 30), kutu_rect, 0, 10)
        pygame.draw.rect(ekran, SARI if giris else GRI, kutu_rect, 3, 10)
        
        # Yazılan metni göster
        if giris:
            text = font.render(giris, True, BEYAZ)
        else:
            text = font.render("Buraya isminizi yazın...", True, GRI)
        text_rect = text.get_rect(center=kutu_rect.center)
        ekran.blit(text, text_rect)
        
        # İmleç
        if pygame.time.get_ticks() % 1000 < 500:
            if giris:
                imlek_x = text_rect.right + 3
            else:
                imlek_x = kutu_rect.left + 15
            pygame.draw.line(ekran, SARI, (imlek_x, kutu_rect.top + 15), (imlek_x, kutu_rect.bottom - 15), 2)
        
        # Kurallar
        kural = kucuk_font.render("2-12 karakter arası", True, GRI)
        kural_rect = kural.get_rect(center=(PENCERE_GENISLIK//2, 300))
        ekran.blit(kural, kural_rect)
        
        # Talimatlar
        enter_aktif = len(giris.strip()) >= 2
        enter_renk = YESIL if enter_aktif else GRI
        enter_text = font.render("ENTER - Tamam", True, enter_renk)
        enter_rect = enter_text.get_rect(center=(PENCERE_GENISLIK//2, 380))
        ekran.blit(enter_text, enter_rect)
        
        esc_text = kucuk_font.render("ESC - Geri Dön", True, GRI)
        esc_rect = esc_text.get_rect(center=(PENCERE_GENISLIK//2, 420))
        ekran.blit(esc_text, esc_rect)
        
        pygame.display.flip()
        
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    return False
                elif olay.key == pygame.K_RETURN:
                    if len(giris.strip()) >= 2:
                        oyuncu_adi = giris.strip()
                        return True
                elif olay.key == pygame.K_BACKSPACE:
                    giris = giris[:-1]
                else:
                    if olay.unicode.isprintable() and len(giris) < 12:
                        giris += olay.unicode

def karakter_sec():
    global secili_karakter
    karakter_isimleri = list(KARAKTERLER.keys())
    secili = karakter_isimleri.index(secili_karakter) if secili_karakter in karakter_isimleri else 0
    
    while True:
        ekran.fill(SIYAH)
        
        # Başlık - modern stil
        baslik = buyuk_font.render('KARAKTER SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        # Modern ayırıcı çizgi
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Karakterleri göster - daha düzenli
        baslangic_y = 160
        for i, isim in enumerate(karakter_isimleri):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            # Karakter kutusu
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            # Modern karakter kutusu tasarımı
            if secili_mi:
                pygame.draw.rect(ekran, KOYU_GRI, kutu_rect, 0, 15)
                pygame.draw.rect(ekran, CYAN, kutu_rect, 4, 15)
            else:
                pygame.draw.rect(ekran, (30, 30, 35), kutu_rect, 0, 15)
                pygame.draw.rect(ekran, ACIK_GRI, kutu_rect, 2, 15)
            
            # Karakter sprite'ını büyük göster
            karakter_sprite = KARAKTERLER[isim]
            buyuk_sprite = pygame.transform.scale(karakter_sprite, (80, 80))
            sprite_rect = buyuk_sprite.get_rect(center=(kutu_x + 80, y + 40))
            ekran.blit(buyuk_sprite, sprite_rect)
            
            # Karakter ismi - modern renkler
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
            # "AKTIF" yazısı - modern yeşil
            if isim == secili_karakter:  # Aktif karakter kontrolü
                aktif_text = kucuk_font.render("AKTIF", True, NEON_YESIL)
                aktif_rect = aktif_text.get_rect(center=(kutu_x + 280, y + 60))
                ekran.blit(aktif_text, aktif_rect)
            
            # Ok işaretleri kaldırıldı - sadece kutu vurgusu yeterli
            if secili_mi:
                pass  # Sadece kutu vurgusu var artık
        
        pygame.display.flip()
        
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    return  # Ayarlar menüsüne dön
                elif olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(karakter_isimleri)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(karakter_isimleri)
                elif olay.key == pygame.K_RETURN:
                    secili_karakter = karakter_isimleri[secili]
                    return

def ana_menu():
    secenekler = ['Oyuna Başla', 'Skor Tablosu', 'Ayarlar', 'Çıkış']
    secili = 0
    
    while True:
        ekran.fill(SIYAH)
        
        # Ana başlık
        baslik = buyuk_font.render('EcoSnake Game', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 100))
        ekran.blit(baslik, baslik_rect)
        
        alt_baslik = font.render('Çevreyi Koruma Oyunu', True, NEON_YESIL)
        alt_rect = alt_baslik.get_rect(center=(PENCERE_GENISLIK//2, 140))
        ekran.blit(alt_baslik, alt_rect)
        
        # Oyuncu bilgileri
        if oyuncu_adi:
            oyuncu_text = kucuk_font.render(f'Oyuncu: {oyuncu_adi}', True, BEYAZ)
            ekran.blit(oyuncu_text, (20, 20))
            karakter_text = kucuk_font.render(f'Karakter: {secili_karakter}', True, BEYAZ)
            ekran.blit(karakter_text, (20, 40))
            arkaplan_text = kucuk_font.render(f'Arkaplan: {secili_arkaplan}', True, BEYAZ)
            ekran.blit(arkaplan_text, (20, 60))
        
        # Menü seçenekleri - modern gradient efekti
        menu_baslangic_y = 220
        for i, secenek in enumerate(secenekler):
            renk = SIYAH if i == secili else ACIK_GRI  # Seçili Siyah, diğerleri açık gri
            y = menu_baslangic_y + i * 60  # Daha ferah aralık
            
            # Seçili seçenek için modern arka plan
            if i == secili:
                # Gradient benzeri efekt için çoklu dikdörtgen
                pygame.draw.rect(ekran, KOYU_GRI, (220, y-25, PENCERE_GENISLIK-440, 50), 0, 12)
                pygame.draw.rect(ekran, CYAN, (220, y-25, PENCERE_GENISLIK-440, 50), 3, 12)
                # İç glow efekti
                pygame.draw.rect(ekran, (26, 188, 156, 50), (225, y-20, PENCERE_GENISLIK-450, 40), 0, 10)
            
            text = font.render(secenek, True, renk)
            text_rect = text.get_rect(center=(PENCERE_GENISLIK//2, y))
            ekran.blit(text, text_rect)
        
        # Talimatlar - daha aşağıda
        talim = kucuk_font.render("Yön tuşları ile seç, ENTER ile onayla, ESC ile çık", True, GRI)
        talim_rect = talim.get_rect(center=(PENCERE_GENISLIK//2, 520))
        ekran.blit(talim, talim_rect)
        
        pygame.display.flip()
        
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(secenekler)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(secenekler)
                elif olay.key == pygame.K_RETURN:
                    if secili == 0:  # Oyuna Başla
                        return 'oyun'
                    elif secili == 1:  # Skor Tablosu
                        skor_tablosu_goster()
                    elif secili == 2:  # Ayarlar
                        return 'ayarlar'
                    elif secili == 3:  # Çıkış
                        pygame.quit()
                        sys.exit()

def ayarlar_menu():
    secenekler = ['Karakter Seç', 'Arkaplan Seç', 'Çöp Poşeti Seç']
    secili = 0
    
    while True:
        ekran.fill(SIYAH)
        
        # Başlık - modern stil
        baslik = buyuk_font.render('AYARLAR', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        # Modern ayırıcı çizgi - gradient efekti
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        pygame.draw.line(ekran, KOYU_GRI, (100, 112), (PENCERE_GENISLIK-100, 112), 1)
        
        # Menü seçenekleri - modern tasarım
        menu_baslangic_y = 160  # Daha yukarıda
        for i, secenek in enumerate(secenekler):
            renk = BEYAZ if i == secili else ACIK_GRI  # Seçili beyaz, diğerleri açık gri
            y = menu_baslangic_y + i * 60  # Daha ferah aralık
            
            # Modern seçili seçenek arka planı
            if i == secili:
                pygame.draw.rect(ekran, KOYU_GRI, (220, y-25, PENCERE_GENISLIK-440, 50), 0, 10)
                pygame.draw.rect(ekran, CYAN, (220, y-25, PENCERE_GENISLIK-440, 50), 3, 10)
            
            text = font.render(secenek, True, renk)
            text_rect = text.get_rect(center=(PENCERE_GENISLIK//2, y))
            ekran.blit(text, text_rect)
            
            if i == secili:
                # Sadece seçili kutusunu vurguladık, ok işaretlerini kaldırdık
                pass
        
        # Geri dön bilgisi
        geri = font.render("Geri dönmek için ESC'ye basın", True, GRI)
        geri_rect = geri.get_rect(center=(PENCERE_GENISLIK//2, 420))
        ekran.blit(geri, geri_rect)
        
        pygame.display.flip()
        
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    return
                elif olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(secenekler)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(secenekler)
                elif olay.key == pygame.K_RETURN:
                    if secili == 0:  # Karakter Seç
                        karakter_sec()
                    elif secili == 1:  # Arkaplan Seç
                        arkaplan_sec()
                    elif secili == 2:  # Çöp Türü Seç
                        garbage_sec()

def arkaplan_sec():
    global secili_arkaplan
    secenekler = ['Siyah', 'Orman']
    secili = secenekler.index(secili_arkaplan) if secili_arkaplan in secenekler else 0
    
    while True:
        ekran.fill(SIYAH)
        
        # Başlık - tutarlı stil
        baslik = buyuk_font.render('ARKAPLAN SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        # Modern ayırıcı çizgi
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Arkaplanları göster - karakter menüsü gibi
        baslangic_y = 160
        for i, isim in enumerate(secenekler):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            # Arkaplan kutusu - karakter menüsü ile aynı ölçüler
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            # Modern arkaplan kutusu
            if secili_mi:
                pygame.draw.rect(ekran, KOYU_GRI, kutu_rect, 0, 15)
                pygame.draw.rect(ekran, CYAN, kutu_rect, 4, 15)
            else:
                pygame.draw.rect(ekran, (30, 30, 35), kutu_rect, 0, 15)
                pygame.draw.rect(ekran, ACIK_GRI, kutu_rect, 2, 15)
            
            # Arkaplan önizlemesi - gerçek resimleri göster, karakter sprite'ı ile aynı pozisyonda
            if isim == 'Siyah':
                # Siyah arkaplan için siyah kare - çerçeve yok
                onizleme_rect = pygame.Rect(0, 0, 80, 80)
                onizleme_rect.center = (kutu_x + 80, y + 40)
                pygame.draw.rect(ekran, SIYAH, onizleme_rect, 0, 5)
            else:  # Orman
                # Gerçek orman resmini küçültüp göster - çerçeve yok
                try:
                    orman_onizleme = pygame.image.load("assets/orman.png")
                    orman_onizleme = pygame.transform.scale(orman_onizleme, (80, 80))
                    # Karakter sprite'ı ile aynı merkez pozisyonu
                    sprite_rect = orman_onizleme.get_rect(center=(kutu_x + 80, y + 40))
                    ekran.blit(orman_onizleme, sprite_rect)
                except:
                    # Resim yüklenemezse basit yeşil kare - çerçeve yok
                    onizleme_rect = pygame.Rect(0, 0, 80, 80)
                    onizleme_rect.center = (kutu_x + 80, y + 40)
                    pygame.draw.rect(ekran, (0, 100, 0), onizleme_rect, 0, 5)
            
            # Arkaplan ismi - modern renkler
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
            # "AKTIF" yazısı - modern yeşil
            if isim == secili_arkaplan:
                aktif_text = kucuk_font.render("AKTIF", True, NEON_YESIL)
                aktif_rect = aktif_text.get_rect(center=(kutu_x + 280, y + 60))
                ekran.blit(aktif_text, aktif_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(secenekler)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(secenekler)
                elif olay.key == pygame.K_RETURN or olay.key == pygame.K_SPACE:
                    secili_arkaplan = secenekler[secili]
                    return
                elif olay.key == pygame.K_ESCAPE:
                    return

def garbage_sec():
    global secili_garbage
    secenekler = list(GARBAGE_TURLERI.keys())
    secili = secenekler.index(secili_garbage) if secili_garbage in secenekler else 0
    
    while True:
        ekran.fill(SIYAH)
        
        # Başlık - modern stil
        baslik = buyuk_font.render('ÇÖP POŞETİ SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        # Modern ayırıcı çizgi
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Poşetleri göster - karakter menüsü gibi
        baslangic_y = 160
        for i, isim in enumerate(secenekler):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            # Poşet kutusu - karakter menüsü ile aynı ölçüler
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            # Modern poşet kutusu
            if secili_mi:
                pygame.draw.rect(ekran, KOYU_GRI, kutu_rect, 0, 15)
                pygame.draw.rect(ekran, CYAN, kutu_rect, 4, 15)
            else:
                pygame.draw.rect(ekran, (30, 30, 35), kutu_rect, 0, 15)
                pygame.draw.rect(ekran, ACIK_GRI, kutu_rect, 2, 15)
            
            # Poşet sprite'ını büyük göster
            garbage_sprite = GARBAGE_TURLERI[isim]
            buyuk_sprite = pygame.transform.scale(garbage_sprite, (80, 80))
            sprite_rect = buyuk_sprite.get_rect(center=(kutu_x + 80, y + 40))
            ekran.blit(buyuk_sprite, sprite_rect)
            
            # Poşet ismi - modern renkler
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
            # "AKTIF" yazısı - modern yeşil
            if isim == secili_garbage:
                aktif_text = kucuk_font.render("AKTIF", True, NEON_YESIL)
                aktif_rect = aktif_text.get_rect(center=(kutu_x + 280, y + 60))
                ekran.blit(aktif_text, aktif_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(secenekler)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(secenekler)
                elif olay.key == pygame.K_RETURN or olay.key == pygame.K_SPACE:
                    secili_garbage = secenekler[secili]
                    return
                elif olay.key == pygame.K_ESCAPE:
                    return

def zorluk_sec():
    secenekler = list(HIZLAR.keys())
    secili = 0
    while True:
        ekran.fill(SIYAH)
        baslik = font.render('Zorluk Seç:', True, BEYAZ)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 150))
        ekran.blit(baslik, baslik_rect)
        
        for i, isim in enumerate(secenekler):
            renk = SARI if i == secili else BEYAZ
            y = 220 + i*50
            secenek = font.render(isim, True, renk)
            secenek_rect = secenek.get_rect(center=(PENCERE_GENISLIK//2, y))
            ekran.blit(secenek, secenek_rect)
        
        # ESC ile çıkış bilgisi
        cikis_bilgi = font.render("Çıkmak için ESC'ye bas", True, GRI)
        cikis_rect = cikis_bilgi.get_rect(center=(PENCERE_GENISLIK//2, 450))
        ekran.blit(cikis_bilgi, cikis_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_UP:
                    secili = (secili - 1) % len(secenekler)
                elif olay.key == pygame.K_DOWN:
                    secili = (secili + 1) % len(secenekler)
                elif olay.key == pygame.K_RETURN or olay.key == pygame.K_SPACE:
                    return HIZLAR[secenekler[secili]], secenekler[secili]
                elif olay.key == pygame.K_ESCAPE:
                    return None, None  # Ana menüye dön

def oyun_bitti_ekrani(skor, zorluk_ismi):
    # Skoru kaydet
    skor_kaydet(oyuncu_adi, skor, secili_karakter, zorluk_ismi)
    
    while True:
        ekran.fill(SIYAH)
        
        # Modern başlık
        baslik = buyuk_font.render('OYUN BITTI!', True, KIRMIZI)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 100))
        ekran.blit(baslik, baslik_rect)
        
        # Oyun sonucu bilgileri - modern renkler
        oyuncu_text = font.render(f'Oyuncu: {oyuncu_adi}', True, CYAN)
        oyuncu_rect = oyuncu_text.get_rect(center=(PENCERE_GENISLIK//2, 170))
        ekran.blit(oyuncu_text, oyuncu_rect)
        
        skor_text = font.render(f'Toplanan Çöp: {skor}', True, NEON_YESIL)
        skor_rect = skor_text.get_rect(center=(PENCERE_GENISLIK//2, 200))
        ekran.blit(skor_text, skor_rect)
        
        zorluk_text = font.render(f'Zorluk: {zorluk_ismi}', True, ACIK_GRI)
        zorluk_rect = zorluk_text.get_rect(center=(PENCERE_GENISLIK//2, 230))
        ekran.blit(zorluk_text, zorluk_rect)
        
        # Çevresel mesaj - modern renk
        sosyal = font.render("Daha temiz bir dünya için çöpünü yere atma!", True, NEON_YESIL)
        sosyal_rect = sosyal.get_rect(center=(PENCERE_GENISLIK//2, 290))
        ekran.blit(sosyal, sosyal_rect)
        
        # Seçenekler
        tekrar = font.render("Tekrar oynamak için ENTER'a bas", True, BEYAZ)
        tekrar_rect = tekrar.get_rect(center=(PENCERE_GENISLIK//2, 350))
        ekran.blit(tekrar, tekrar_rect)
        
        skor_goster = font.render("Skor tablosunu görmek için S'ye bas", True, BEYAZ)
        skor_goster_rect = skor_goster.get_rect(center=(PENCERE_GENISLIK//2, 380))
        ekran.blit(skor_goster, skor_goster_rect)
        
        menu = font.render("Ana menü için M'ye bas", True, BEYAZ)
        menu_rect = menu.get_rect(center=(PENCERE_GENISLIK//2, 410))
        ekran.blit(menu, menu_rect)
        
        cikis = font.render("Çıkmak için ESC'ye bas", True, GRI)
        cikis_rect = cikis.get_rect(center=(PENCERE_GENISLIK//2, 470))
        ekran.blit(cikis, cikis_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_RETURN:
                    return 'tekrar'
                elif olay.key == pygame.K_s:
                    skor_tablosu_goster()
                elif olay.key == pygame.K_m:
                    return 'menu'
                elif olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global FPS, oyuncu_adi, secili_karakter, secili_arkaplan
    
    while True:
        # Ana menüyü göster
        menu_secim = ana_menu()
        
        if menu_secim == 'ayarlar':
            ayarlar_menu()
            continue
        elif menu_secim != 'oyun':
            continue
        
        # Oyuncu adı kontrolü ve zorluk seçimi döngüsü
        oyun_hizi = None  # Başlangıç değeri
        zorluk_ismi = None  # Başlangıç değeri
        
        while True:
            # Her oyuna girmeden önce isim sor
            if not isim_gir():  # ESC ile çıkılmışsa
                break  # Ana menüye dön
            
            # Zorluk seçimi
            oyun_hizi, zorluk_ismi = zorluk_sec()  # Hareket hızı ve zorluk ismi
            
            # Zorluk seçiminde ESC ile çıkış kontrolü
            if oyun_hizi is None or zorluk_ismi is None:
                # Zorluk seçiminde ESC'ye basılmışsa, isim girme ekranına dön
                oyuncu_adi = ""  # İsmi sıfırla, tekrar isim girme ekranına git
                continue
            else:
                break  # Zorluk seçildi, oyuna geç
        
        # Eğer bu noktaya gelmişse, ya ESC ile çıkılmış ya da zorluk seçilmiş
        if oyun_hizi is None or zorluk_ismi is None:
            continue  # Ana menüye dön
        
        # Oyun döngüsü
        while True:
            toplayici = CopToplayici(KARAKTERLER[secili_karakter])
            cop = Cop()
            skor = 0
            son_yon = (1, 0)
            buyu = False
            oyun_bitti = False
            ana_menuye_don = False
            frame_sayac = 0  # Hareket kontrolü için sayaç
            
            while not oyun_bitti and not ana_menuye_don:
                for olay in pygame.event.get():
                    if olay.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if olay.type == pygame.KEYDOWN:
                        # ESC tuşu ile ana menüye dönüş
                        if olay.key == pygame.K_ESCAPE:
                            ana_menuye_don = True
                            break
                        
                        yeni_yon = None
                        if olay.key == pygame.K_UP and son_yon != (0, 1):
                            yeni_yon = (0, -1)
                        elif olay.key == pygame.K_DOWN and son_yon != (0, -1):
                            yeni_yon = (0, 1)
                        elif olay.key == pygame.K_LEFT and son_yon != (1, 0):
                            yeni_yon = (-1, 0)
                        elif olay.key == pygame.K_RIGHT and son_yon != (-1, 0):
                            yeni_yon = (1, 0)
                        if yeni_yon:
                            toplayici.yon_x, toplayici.yon_y = yeni_yon
                            son_yon = yeni_yon

                # Frame sayacı artır
                frame_sayac += 1
                
                # Hareket kontrolü - sadece belirli frame aralıklarında hareket et
                hareket_zamani = False
                if frame_sayac >= (60 // oyun_hizi):  # 60 FPS bazında hareket hızı
                    frame_sayac = 0
                    hareket_zamani = True
                    
                    # Hareketten önce kuyruğu sakla (büyüme için)
                    eski_kuyruk = toplayici.kareler[-1]
                    toplayici.hareket_et()
                
                # Her frame'de çarpışma kontrolü (çok önemli!)
                bas_x, bas_y = toplayici.kareler[0]
                
                # Çöp yeme kontrolü - TOLERANCE ile (daha güvenilir)
                carpisma_var = (abs(bas_x - cop.x) <= KARE_BOYUT//2) and (abs(bas_y - cop.y) <= KARE_BOYUT//2)
                
                if carpisma_var:
                    if hareket_zamani:
                        # Hareket frame'inde: eski kuyruk ile büyü
                        toplayici.kareler.append(eski_kuyruk)
                    else:
                        # Diğer frame'lerde: son kare ile büyü
                        toplayici.kareler.append(toplayici.kareler[-1])
                    
                    skor += 1
                    cop = Cop()  # Yeni çöp oluştur
                
                # Kendine çarpma kontrolü - sadece hareket frame'inde
                if hareket_zamani:
                    if toplayici.carpisma_kontrolu():
                        oyun_bitti = True

                # Arkaplanı çiz
                if secili_arkaplan == 'Orman':
                    ekran.blit(orman_arkaplan, (0, 0))
                else:
                    ekran.fill(SIYAH)
                    
                toplayici.ciz(ekran)
                cop.ciz(ekran)
                
                # Modern UI arka plan
                pygame.draw.rect(ekran, KOYU_GRI, (0, 0, PENCERE_GENISLIK, 45))
                pygame.draw.rect(ekran, SIYAH, (0, 43, PENCERE_GENISLIK, 2))  # Alt çizgi
                
                # Sol üst - Oyuncu ve skor bilgisi (modern renkler)
                oyuncu_text = kucuk_font.render(f"{oyuncu_adi}: {skor} çöp", True, ACIK_GRI)
                ekran.blit(oyuncu_text, (10, 10))
                
                # Sağ üst - ESC bilgisi (modern renkler)
                esc_bilgi = kucuk_font.render("ESC: Ana Menü", True, ACIK_GRI)
                ekran.blit(esc_bilgi, (PENCERE_GENISLIK - 130, 15))
                
                pygame.display.flip()
                saat.tick(60)  # Sabit 60 FPS için akıcılık
        
            # Eğer ana menüye dönülmek isteniyorsa oyun döngüsünden çık
            if ana_menuye_don:
                break
                
            # Oyun bittiğinde sonuç ekranını göster
            if oyun_bitti:
                sonuc = oyun_bitti_ekrani(skor, zorluk_ismi)
                if sonuc == 'tekrar':
                    continue  # Aynı ayarlarla tekrar oyna
                elif sonuc == 'menu':
                    break  # Ana menüye dön
            
            break  # Normal çıkış

if __name__ == "__main__":
    main()