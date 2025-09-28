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
pygame.init()

# Renk Paleti
SIYAH = (20, 20, 30)
BEYAZ = (250, 250, 255)
YESIL = (46, 204, 113)
KIRMIZI = (231, 76, 60)
MAVI = (52, 152, 219)
KAHVERENGI = (160, 116, 85)
SARI = (241, 196, 15)
GRI = (149, 165, 166)
NEON_YESIL = (39, 174, 96)
MOR = (155, 89, 182)
TURUNCU = (230, 126, 34)
CYAN = (26, 188, 156)
KOYU_GRI = (52, 73, 94)
ACIK_GRI = (200, 210, 215)

# Oyun ayarları
PENCERE_GENISLIK = 800
PENCERE_YUKSEKLIK = 600
KARE_BOYUT = 30

HIZLAR = {
    'Kolay': 4,
    'Orta': 9,
    'Zor': 15
}

# Zorluk renkleri
ZORLUK_RENKLERI = {
    'Kolay': YESIL,
    'Orta': TURUNCU, 
    'Zor': KIRMIZI
}
FPS = 60

ekran = pygame.display.set_mode((PENCERE_GENISLIK, PENCERE_YUKSEKLIK))
pygame.display.set_caption("EcoSnake-Game")
saat = pygame.time.Clock()


# Sprite yükleme fonksiyonu
def sprite_yukle(dosya_adi, boyut=(KARE_BOYUT, KARE_BOYUT)):
    sprite = pygame.image.load(f"assets/{dosya_adi}")
    return pygame.transform.scale(sprite, boyut)

# Karakterler
KARAKTERLER = {
    'Bahçıvan': sprite_yukle("gardener.png"),
    'HakanTema': sprite_yukle("hakantema.png"),
    'Tombik Çocuk': sprite_yukle("obesity.png")
}

# Çöp türleri
COP_SPRITES = {
    'apple': sprite_yukle("apple.png"),
    'banana': sprite_yukle("banana.png"),
    'bottle': sprite_yukle("bottle.png"),
    'landfill': sprite_yukle("landfill.png")
}

# Çöp poşetleri
GARBAGE_TURLERI = {
    'Tatlı Poşet': sprite_yukle("garbage1.png"),
    'Sarı Poşet': sprite_yukle("garbage2.png"),
    'Siyah Poşet': sprite_yukle("garbage3.png")
}

# Arkaplanlar
ARKAPLANLAR = {
    'Orman': sprite_yukle("orman.png", (PENCERE_GENISLIK, PENCERE_YUKSEKLIK)),
    'Sahil': sprite_yukle("beach.png", (PENCERE_GENISLIK, PENCERE_YUKSEKLIK))
}

# Font oluştur
font = pygame.font.Font(None, 36)
buyuk_font = pygame.font.Font(None, 48)
kucuk_font = pygame.font.Font(None, 24)

# Menü yardımcı fonksiyonlar
def menu_kutusu_ciz(ekran, kutu_rect, secili=False):
    if secili:
        pygame.draw.rect(ekran, KOYU_GRI, kutu_rect, 0, 15)
        pygame.draw.rect(ekran, CYAN, kutu_rect, 4, 15)
    else:
        pygame.draw.rect(ekran, (30, 30, 35), kutu_rect, 0, 15)
        pygame.draw.rect(ekran, ACIK_GRI, kutu_rect, 2, 15)

def skor_satiri_ciz(ekran, i, skor_bilgi, y_pos, pozisyonlar):
    renkler = [SARI, ACIK_GRI, TURUNCU, CYAN, CYAN, GRI, GRI, GRI, GRI, GRI]
    renk = renkler[i] if i < len(renkler) else GRI
    
    texts = [f"{i+1}.", skor_bilgi['isim'][:12], str(skor_bilgi['skor']), skor_bilgi['zorluk']]
    for text, x_pos in zip(texts, pozisyonlar):
        text_surface = kucuk_font.render(text, True, renk)
        ekran.blit(text_surface, (x_pos, y_pos))

# Oyuncu verileri
oyuncu_adi = ""
secili_karakter = "Bahçıvan"
secili_arkaplan = "Siyah"
secili_garbage = "Tatlı Poşet"

class CopToplayici:
    def __init__(self, karakter_sprite):
        self.yon_x = 1
        self.yon_y = 0
        self.kareler = []
        self.karakter_sprite = karakter_sprite
        baslangic_x = (PENCERE_GENISLIK // 2 // KARE_BOYUT) * KARE_BOYUT
        baslangic_y = (PENCERE_YUKSEKLIK // 2 // KARE_BOYUT) * KARE_BOYUT
        self.kareler.append((baslangic_x, baslangic_y))

    def hareket_et(self):
        bas_x, bas_y = self.kareler[0]
        yeni_x = bas_x + self.yon_x * KARE_BOYUT
        yeni_y = bas_y + self.yon_y * KARE_BOYUT
        
        UI_ALAN_YUKSEKLIK = 45
        
        if yeni_x < 0:
            yeni_x = PENCERE_GENISLIK - KARE_BOYUT
        elif yeni_x >= PENCERE_GENISLIK:
            yeni_x = 0
            
        if yeni_y < UI_ALAN_YUKSEKLIK:
            yeni_y = PENCERE_YUKSEKLIK - KARE_BOYUT
        elif yeni_y >= PENCERE_YUKSEKLIK:
            yeni_y = UI_ALAN_YUKSEKLIK
            
        yeni_bas = (yeni_x, yeni_y)
        self.kareler = [yeni_bas] + self.kareler[:-1]

    def cop_topla(self):
        self.kareler.append(self.kareler[-1])

    def ciz(self, ekran):
        bas_x, bas_y = self.kareler[0]
        ekran.blit(self.karakter_sprite, (bas_x, bas_y))
        secili_garbage_sprite = GARBAGE_TURLERI[secili_garbage]
        for (x, y) in self.kareler[1:]:
            ekran.blit(secili_garbage_sprite, (x, y))

    def carpisma_kontrolu(self):
        bas = self.kareler[0]
        return bas in self.kareler[1:]

class Cop:
    def __init__(self):
        min_x = 1
        max_x = (PENCERE_GENISLIK // KARE_BOYUT) - 2
        min_y = 3
        max_y = (PENCERE_YUKSEKLIK // KARE_BOYUT) - 2
        
        self.x = random.randint(min_x, max_x) * KARE_BOYUT
        self.y = random.randint(min_y, max_y) * KARE_BOYUT
        
        self.tur = random.choice(list(COP_SPRITES.keys()))
        self.sprite = COP_SPRITES[self.tur]
    
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
    skorlar = skorlar[:10]
    
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
            y_pos = 130
            pozisyonlar = [150, 200, 400, 500]
            basliklar = ['No.', 'İsim', 'Skor', 'Zorluk']
            
            for baslik, x_pos in zip(basliklar, pozisyonlar):
                text = kucuk_font.render(baslik, True, BEYAZ)
                ekran.blit(text, (x_pos, y_pos))
            
            y_pos += 25
            pygame.draw.line(ekran, BEYAZ, (pozisyonlar[0], y_pos), (pozisyonlar[-1] + 80, y_pos), 1)
            y_pos += 15
            
            for i, skor_bilgi in enumerate(skorlar[:10]):
                skor_satiri_ciz(ekran, i, skor_bilgi, y_pos, pozisyonlar)
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
        
        baslik = buyuk_font.render('KARAKTER SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Karakterleri göster
        baslangic_y = 160
        for i, isim in enumerate(karakter_isimleri):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            menu_kutusu_ciz(ekran, kutu_rect, secili_mi)
            
            # Karakter sprite'ını göster
            karakter_sprite = KARAKTERLER[isim]
            buyuk_sprite = pygame.transform.scale(karakter_sprite, (80, 80))
            sprite_rect = buyuk_sprite.get_rect(center=(kutu_x + 80, y + 40))
            ekran.blit(buyuk_sprite, sprite_rect)
            
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
            if isim == secili_karakter:
                aktif_text = kucuk_font.render("AKTIF", True, NEON_YESIL)
                aktif_rect = aktif_text.get_rect(center=(kutu_x + 280, y + 60))
                ekran.blit(aktif_text, aktif_rect)
        
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
        
        # Menü seçenekleri
        menu_baslangic_y = 220
        for i, secenek in enumerate(secenekler):
            renk = BEYAZ if i == secili else ACIK_GRI
            y = menu_baslangic_y + i * 60
            
            if i == secili:
                pygame.draw.rect(ekran, KOYU_GRI, (220, y-25, PENCERE_GENISLIK-440, 50), 0, 12)
                pygame.draw.rect(ekran, CYAN, (220, y-25, PENCERE_GENISLIK-440, 50), 3, 12)
                pygame.draw.rect(ekran, (52, 73, 94), (225, y-20, PENCERE_GENISLIK-450, 40), 0, 10)
            
            text = font.render(secenek, True, renk)
            text_rect = text.get_rect(center=(PENCERE_GENISLIK//2, y))
            ekran.blit(text, text_rect)
        
        # Talimatlar
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
        
        baslik = buyuk_font.render('AYARLAR', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        pygame.draw.line(ekran, KOYU_GRI, (100, 112), (PENCERE_GENISLIK-100, 112), 1)
        
        # Menü seçenekleri
        menu_baslangic_y = 160
        for i, secenek in enumerate(secenekler):
            renk = BEYAZ if i == secili else ACIK_GRI
            y = menu_baslangic_y + i * 60
            
            if i == secili:
                pygame.draw.rect(ekran, KOYU_GRI, (220, y-25, PENCERE_GENISLIK-440, 50), 0, 10)
                pygame.draw.rect(ekran, CYAN, (220, y-25, PENCERE_GENISLIK-440, 50), 3, 10)
            
            text = font.render(secenek, True, renk)
            text_rect = text.get_rect(center=(PENCERE_GENISLIK//2, y))
            ekran.blit(text, text_rect)
        
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
    secenekler = ['Siyah', 'Orman', 'Sahil']
    secili = secenekler.index(secili_arkaplan) if secili_arkaplan in secenekler else 0
    
    while True:
        ekran.fill(SIYAH)
        
        baslik = buyuk_font.render('ARKAPLAN SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Arkaplanları göster
        baslangic_y = 160
        for i, isim in enumerate(secenekler):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            menu_kutusu_ciz(ekran, kutu_rect, secili_mi)
            
            # Arkaplan önizlemesi
            if isim == 'Siyah':
                onizleme_rect = pygame.Rect(0, 0, 80, 80)
                onizleme_rect.center = (kutu_x + 80, y + 40)
                pygame.draw.rect(ekran, SIYAH, onizleme_rect, 0, 5)
            elif isim in ARKAPLANLAR:
                try:
                    onizleme = pygame.transform.scale(ARKAPLANLAR[isim], (80, 80))
                    sprite_rect = onizleme.get_rect(center=(kutu_x + 80, y + 40))
                    ekran.blit(onizleme, sprite_rect)
                except:
                    renk = (0, 100, 0) if isim == 'Orman' else (30, 144, 255)
                    onizleme_rect = pygame.Rect(0, 0, 80, 80)
                    onizleme_rect.center = (kutu_x + 80, y + 40)
                    pygame.draw.rect(ekran, renk, onizleme_rect, 0, 5)
            
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
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
        
        baslik = buyuk_font.render('ÇÖP POŞETİ SEÇ', True, CYAN)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 80))
        ekran.blit(baslik, baslik_rect)
        
        pygame.draw.line(ekran, CYAN, (100, 110), (PENCERE_GENISLIK-100, 110), 3)
        
        # Poşetleri göster
        baslangic_y = 160
        for i, isim in enumerate(secenekler):
            y = baslangic_y + i * 140
            secili_mi = (i == secili)
            
            kutu_genislik = 500
            kutu_yukseklik = 120
            kutu_x = PENCERE_GENISLIK//2 - kutu_genislik//2
            kutu_rect = pygame.Rect(kutu_x, y-20, kutu_genislik, kutu_yukseklik)
            
            menu_kutusu_ciz(ekran, kutu_rect, secili_mi)
            
            # Poşet sprite'ını göster
            garbage_sprite = GARBAGE_TURLERI[isim]
            buyuk_sprite = pygame.transform.scale(garbage_sprite, (80, 80))
            sprite_rect = buyuk_sprite.get_rect(center=(kutu_x + 80, y + 40))
            ekran.blit(buyuk_sprite, sprite_rect)
            
            renk = CYAN if secili_mi else BEYAZ
            isim_text = font.render(isim, True, renk)
            isim_rect = isim_text.get_rect(center=(kutu_x + 280, y + 30))
            ekran.blit(isim_text, isim_rect)
            
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
            zorluk_rengi = ZORLUK_RENKLERI[isim]
            if i == secili:
                # Seçili zorluk için kutu çiz
                pygame.draw.rect(ekran, KOYU_GRI, (PENCERE_GENISLIK//2 - 100, 220 + i*50 - 20, 200, 40), 0, 10)
                pygame.draw.rect(ekran, zorluk_rengi, (PENCERE_GENISLIK//2 - 100, 220 + i*50 - 20, 200, 40), 3, 10)
                renk = zorluk_rengi
            else:
                renk = zorluk_rengi
                
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
    skor_kaydet(oyuncu_adi, skor, secili_karakter, zorluk_ismi)
    
    while True:
        ekran.fill(SIYAH)

        baslik = buyuk_font.render('OYUN BİTTİ!', True, KIRMIZI)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 100))
        ekran.blit(baslik, baslik_rect)
        
        # Oyun sonucu bilgileri
        oyuncu_text = font.render(f'Oyuncu: {oyuncu_adi}', True, MOR)
        oyuncu_rect = oyuncu_text.get_rect(center=(PENCERE_GENISLIK//2, 170))
        ekran.blit(oyuncu_text, oyuncu_rect)
        
        skor_text = font.render(f'Toplanan Çöp: {skor}', True, NEON_YESIL)
        skor_rect = skor_text.get_rect(center=(PENCERE_GENISLIK//2, 200))
        ekran.blit(skor_text, skor_rect)
        
        zorluk_rengi = ZORLUK_RENKLERI.get(zorluk_ismi, ACIK_GRI)
        
        # "Zorluk:" etiketini beyaz yaz
        zorluk_etiket = font.render('Zorluk: ', True, BEYAZ)
        zorluk_etiket_rect = zorluk_etiket.get_rect()
        
        # Zorluk seviyesini renkli yaz
        zorluk_seviye = font.render(zorluk_ismi, True, zorluk_rengi)
        zorluk_seviye_rect = zorluk_seviye.get_rect()
        
        # İki metni yan yana hizala
        toplam_genislik = zorluk_etiket_rect.width + zorluk_seviye_rect.width
        baslangic_x = (PENCERE_GENISLIK - toplam_genislik) // 2
        
        zorluk_etiket_rect.x = baslangic_x
        zorluk_etiket_rect.centery = 230
        ekran.blit(zorluk_etiket, zorluk_etiket_rect)
        
        zorluk_seviye_rect.x = baslangic_x + zorluk_etiket_rect.width
        zorluk_seviye_rect.centery = 230
        ekran.blit(zorluk_seviye, zorluk_seviye_rect)
        
        sosyal = font.render("Daha temiz bir dünya için çöpünü yere atma!", True, NEON_YESIL)
        sosyal_rect = sosyal.get_rect(center=(PENCERE_GENISLIK//2, 290))
        ekran.blit(sosyal, sosyal_rect)
        
        # Seçenekleri vurgulu şekilde çiz
        
        # ENTER seçeneği
        enter_text1 = font.render("Tekrar oynamak için ", True, BEYAZ)
        enter_text2 = font.render("ENTER", True, SARI)
        enter_text3 = font.render("'a bas", True, BEYAZ)
        
        toplam_genislik = enter_text1.get_width() + enter_text2.get_width() + enter_text3.get_width()
        baslangic_x = (PENCERE_GENISLIK - toplam_genislik) // 2
        
        ekran.blit(enter_text1, (baslangic_x, 350))
        ekran.blit(enter_text2, (baslangic_x + enter_text1.get_width(), 350))
        ekran.blit(enter_text3, (baslangic_x + enter_text1.get_width() + enter_text2.get_width(), 350))
        
        # S seçeneği
        s_text1 = font.render("Skor tablosunu görmek için ", True, BEYAZ)
        s_text2 = font.render("S", True, SARI)
        s_text3 = font.render("'ye bas", True, BEYAZ)
        
        toplam_genislik = s_text1.get_width() + s_text2.get_width() + s_text3.get_width()
        baslangic_x = (PENCERE_GENISLIK - toplam_genislik) // 2
        
        ekran.blit(s_text1, (baslangic_x, 380))
        ekran.blit(s_text2, (baslangic_x + s_text1.get_width(), 380))
        ekran.blit(s_text3, (baslangic_x + s_text1.get_width() + s_text2.get_width(), 380))
        
        # M seçeneği
        m_text1 = font.render("Ana menü için ", True, BEYAZ)
        m_text2 = font.render("M", True, SARI)
        m_text3 = font.render("'ye bas", True, BEYAZ)
        
        toplam_genislik = m_text1.get_width() + m_text2.get_width() + m_text3.get_width()
        baslangic_x = (PENCERE_GENISLIK - toplam_genislik) // 2
        
        ekran.blit(m_text1, (baslangic_x, 410))
        ekran.blit(m_text2, (baslangic_x + m_text1.get_width(), 410))
        ekran.blit(m_text3, (baslangic_x + m_text1.get_width() + m_text2.get_width(), 410))
        
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
        menu_secim = ana_menu()
        
        if menu_secim == 'ayarlar':
            ayarlar_menu()
            continue
        elif menu_secim != 'oyun':
            continue
        
        # Oyuncu adı ve zorluk seçimi
        oyun_hizi = None
        zorluk_ismi = None
        
        while True:
            if not isim_gir():
                break
            
            oyun_hizi, zorluk_ismi = zorluk_sec()
            
            if oyun_hizi is None or zorluk_ismi is None:
                oyuncu_adi = ""
                continue
            else:
                break
        
        if oyun_hizi is None or zorluk_ismi is None:
            continue
        
        # Oyun döngüsü
        while True:
            toplayici = CopToplayici(KARAKTERLER[secili_karakter])
            cop = Cop()
            skor = 0
            son_yon = (1, 0)
            buyu = False
            oyun_bitti = False
            ana_menuye_don = False
            frame_sayac = 0
            
            while not oyun_bitti and not ana_menuye_don:
                for olay in pygame.event.get():
                    if olay.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if olay.type == pygame.KEYDOWN:
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

                frame_sayac += 1
                
                hareket_zamani = False
                if frame_sayac >= (60 // oyun_hizi):
                    frame_sayac = 0
                    hareket_zamani = True
                    eski_kuyruk = toplayici.kareler[-1]
                    toplayici.hareket_et()
                
                bas_x, bas_y = toplayici.kareler[0]
                
                carpisma_var = (abs(bas_x - cop.x) <= KARE_BOYUT//2) and (abs(bas_y - cop.y) <= KARE_BOYUT//2)
                
                if carpisma_var:
                    if hareket_zamani:
                        toplayici.kareler.append(eski_kuyruk)
                    else:
                        toplayici.kareler.append(toplayici.kareler[-1])
                    
                    skor += 1
                    cop = Cop()
                
                if hareket_zamani:
                    if toplayici.carpisma_kontrolu():
                        oyun_bitti = True

                # Arkaplanı çiz
                if secili_arkaplan in ARKAPLANLAR:
                    ekran.blit(ARKAPLANLAR[secili_arkaplan], (0, 0))
                else:
                    ekran.fill(SIYAH)
                    
                toplayici.ciz(ekran)
                cop.ciz(ekran)
                
                pygame.draw.rect(ekran, KOYU_GRI, (0, 0, PENCERE_GENISLIK, 45))
                pygame.draw.rect(ekran, ACIK_GRI, (0, 43, PENCERE_GENISLIK, 2))
                
                oyuncu_text = kucuk_font.render(f"{oyuncu_adi}: {skor} çöp", True, ACIK_GRI)
                ekran.blit(oyuncu_text, (10, 10))
                
                esc_bilgi = kucuk_font.render("ESC: Ana Menü", True, ACIK_GRI)
                ekran.blit(esc_bilgi, (PENCERE_GENISLIK - 130, 15))
                
                pygame.display.flip()
                saat.tick(60)
        
            if ana_menuye_don:
                break
                
            if oyun_bitti:
                sonuc = oyun_bitti_ekrani(skor, zorluk_ismi)
                if sonuc == 'tekrar':
                    continue
                elif sonuc == 'menu':
                    break
            
            break

if __name__ == "__main__":
    main()
