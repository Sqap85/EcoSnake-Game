import pygame
import os
import random
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Pygame'i başlat
pygame.init()

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 255, 0)
KIRMIZI = (255, 0, 0)
MAVI = (0, 0, 255)
KAHVERENGI = (139, 69, 19)
SARI = (255, 255, 0)
GRI = (128, 128, 128)

# Oyun ayarları
PENCERE_GENISLIK = 800
PENCERE_YUKSEKLIK = 600
KARE_BOYUT = 30

# Hız/zorluk seçenekleri (oyun hızı, düşük = daha yavaş hareket)
HIZLAR = {
    'Kolay': 8,    # Daha yavaş hareket (saniyede 8 hareket)
    'Orta': 12,    # Normal hareket hızı (saniyede 12 hareket)  
    'Zor': 18      # Hızlı hareket (saniyede 18 hareket)
}
FPS = 60  # Ekran yenileme hızı (akıcılık için yüksek tutulmalı)

# Ekranı oluştur
ekran = pygame.display.set_mode((PENCERE_GENISLIK, PENCERE_YUKSEKLIK))
pygame.display.set_caption("Çöp Toplama Oyunu")
saat = pygame.time.Clock()


# Görselleri yükle
insan_sprite = pygame.image.load("insan.png")
insan_sprite = pygame.transform.scale(insan_sprite, (KARE_BOYUT, KARE_BOYUT))
cop_sprite = pygame.image.load("cop.png")
cop_sprite = pygame.transform.scale(cop_sprite, (KARE_BOYUT, KARE_BOYUT))

# Çeşitli çöp türleri için sprite'lar
apple_sprite = pygame.image.load("apple.png")
apple_sprite = pygame.transform.scale(apple_sprite, (KARE_BOYUT, KARE_BOYUT))
banana_sprite = pygame.image.load("banana.png")
banana_sprite = pygame.transform.scale(banana_sprite, (KARE_BOYUT, KARE_BOYUT))
bottle_sprite = pygame.image.load("bottle.png")
bottle_sprite = pygame.transform.scale(bottle_sprite, (KARE_BOYUT, KARE_BOYUT))
landfill_sprite = pygame.image.load("landfill.png")
landfill_sprite = pygame.transform.scale(landfill_sprite, (KARE_BOYUT, KARE_BOYUT))

# Font oluştur
font = pygame.font.Font(None, 36)

class CopToplayici:
    def __init__(self):
        self.yon_x = 1
        self.yon_y = 0
        self.kareler = []  # [(x, y), ...] ilk eleman baş (insan), diğerleri poşet
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
        # Baş (insan): sprite ile çiz
        bas_x, bas_y = self.kareler[0]
        ekran.blit(insan_sprite, (bas_x, bas_y))
        # Gövde (çöp poşeti): sprite ile çiz
        for (x, y) in self.kareler[1:]:
            ekran.blit(cop_sprite, (x, y))

    def carpisma_kontrolu(self):
        # Baş gövdeye çarptı mı?
        bas = self.kareler[0]
        return bas in self.kareler[1:]

class Cop:
    def __init__(self):
        # UI yazılarının olduğu alanları hariç tut (üst 45 piksel)
        self.x = random.randint(0, (PENCERE_GENISLIK // KARE_BOYUT) - 1) * KARE_BOYUT
        self.y = random.randint(3, (PENCERE_YUKSEKLIK // KARE_BOYUT) - 1) * KARE_BOYUT  # En az 60 piksel aşağıdan başla
        
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
                    return HIZLAR[secenekler[secili]]
                elif olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def oyun_bitti_ekrani(skor):
    while True:
        ekran.fill(SIYAH)
        mesaj = font.render(f"Tebrikler! Topladığın çöp: {skor}", True, YESIL)
        mesaj_rect = mesaj.get_rect(center=(PENCERE_GENISLIK//2, 180))
        ekran.blit(mesaj, mesaj_rect)
        
        sosyal = font.render("Daha temiz bir dünya için çöpünü yere atma!", True, SARI)
        sosyal_rect = sosyal.get_rect(center=(PENCERE_GENISLIK//2, 240))
        ekran.blit(sosyal, sosyal_rect)
        
        tekrar = font.render("Tekrar oynamak için ENTER'a bas", True, MAVI)
        tekrar_rect = tekrar.get_rect(center=(PENCERE_GENISLIK//2, 320))
        ekran.blit(tekrar, tekrar_rect)
        
        cikis = font.render("Çıkmak için ESC'ye bas", True, GRI)
        cikis_rect = cikis.get_rect(center=(PENCERE_GENISLIK//2, 370))
        ekran.blit(cikis, cikis_rect)
        
        pygame.display.flip()
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_RETURN:
                    return True
                elif olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def bilgi_ekrani():
    while True:
        ekran.fill(SIYAH)
        baslik = font.render("Çöp Toplama Oyunu", True, SARI)
        baslik_rect = baslik.get_rect(center=(PENCERE_GENISLIK//2, 100))
        ekran.blit(baslik, baslik_rect)
        
        bilgi1 = font.render("Şehrimizi ve doğamızı temiz tutmak için çöpleri topla!", True, BEYAZ)
        bilgi1_rect = bilgi1.get_rect(center=(PENCERE_GENISLIK//2, 180))
        ekran.blit(bilgi1, bilgi1_rect)
        
        bilgi2 = font.render("Ok tuşlarıyla hareket et, çöpü topla, poşetine çarpma!", True, BEYAZ)
        bilgi2_rect = bilgi2.get_rect(center=(PENCERE_GENISLIK//2, 230))
        ekran.blit(bilgi2, bilgi2_rect)
        
        sosyal = font.render("Çevreyi korumak senin elinde!", True, YESIL)
        sosyal_rect = sosyal.get_rect(center=(PENCERE_GENISLIK//2, 300))
        ekran.blit(sosyal, sosyal_rect)
        
        # Buraya istediğin sosyal mesajı yazabilirsin
        sosyal2 = font.render("TEMA HAKANI BAŞKAN SEÇ, VER YETKİYİ GÖR ETKİYİ!!!", True, YESIL)
        sosyal2_rect = sosyal2.get_rect(center=(PENCERE_GENISLIK//2, 340))
        ekran.blit(sosyal2, sosyal2_rect)
        
        basla = font.render("Başlamak için ENTER'a bas", True, MAVI)
        basla_rect = basla.get_rect(center=(PENCERE_GENISLIK//2, 380))
        ekran.blit(basla, basla_rect)
        
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
                if olay.key == pygame.K_RETURN:
                    return
                elif olay.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global FPS
    while True:
        bilgi_ekrani()
        oyun_hizi = zorluk_sec()  # Hareket hızı, FPS değil
        
        # Oyun döngüsü
        oyun_devam = True
        while oyun_devam:
            toplayici = CopToplayici()
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
                if frame_sayac >= (60 // oyun_hizi):  # 60 FPS bazında hareket hızı
                    frame_sayac = 0
                    
                    # Hareketten önce kuyruğu sakla (büyüme için)
                    eski_kuyruk = toplayici.kareler[-1]
                    toplayici.hareket_et()
                    
                    # Hareket sonrası çarpışma kontrolleri
                    bas_x, bas_y = toplayici.kareler[0]
                    
                    # Debug: pozisyonları yazdır (geçici)
                    # print(f"Karakter: ({bas_x}, {bas_y}), Çöp: ({cop.x}, {cop.y})")
                    
                    # Çöp yeme kontrolü
                    if bas_x == cop.x and bas_y == cop.y:
                        # Büyüme: eski kuyruğu geri ekle
                        toplayici.kareler.append(eski_kuyruk)
                        skor += 1
                        cop = Cop()  # Yeni çöp oluştur
                        # print(f"Çöp yenildi! Skor: {skor}")  # Debug
                    
                    # Kendine çarpma kontrolü
                    if toplayici.carpisma_kontrolu():
                        oyun_bitti = True

                ekran.fill(SIYAH)
                toplayici.ciz(ekran)
                cop.ciz(ekran)
                
                # UI arka plan alanı (üst kısım için koyu gri arka plan)
                pygame.draw.rect(ekran, (30, 30, 30), (0, 0, PENCERE_GENISLIK, 45))
                
                # Skor ve çıkış bilgisi
                skor_metni = font.render(f"Çöp Sayısı: {skor}", True, BEYAZ)
                ekran.blit(skor_metni, (10, 10))
                
                # Oyun sırasında ESC bilgisi (küçük font ile)
                kucuk_font = pygame.font.Font(None, 24)
                esc_bilgi = kucuk_font.render("ESC: Çıkış", True, BEYAZ)
                ekran.blit(esc_bilgi, (PENCERE_GENISLIK - 120, 15))
                
                pygame.display.flip()
                saat.tick(60)  # Sabit 60 FPS için akıcılık
        
            # Eğer ana menüye dönülmek isteniyorsa oyun döngüsünden çık
            if ana_menuye_don:
                break
                
            if not oyun_bitti_ekrani(skor):
                oyun_devam = False
                break

if __name__ == "__main__":
    main()