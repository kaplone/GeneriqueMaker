#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import shutil
import subprocess
import time
import pickle
import glob
import codecs

import pair_000

dico = {}
dico["nom_base"] = 0

def __init__():
    
    sys.path.append("/home/autor/Desktop/auto-ring")
    
    liste_des_fichiers_propre = []
    
    #### liste des images du generique (panneaux)
    
    #### duree totale, duree de chaque panneau
    
    #### liste d'images finale (pregene + fades + panneaux)
    
    #### generation des fondus
    
    files = glob.glob('/mnt/ramdisk/*')
    for f in files:
        os.remove(f)
    
def nouveauGenerique(n):
    dico["nom_base"] = n
    
def creerGenerique(f):
    
    print(f)
    g_save = open("/home/autor/Desktop/auto-ring/GENERIQUES/temp/%s.abw" % dico["nom_base"], "w")
    g_save.write(f)
    g_save.close()
    g_temp = open("/home/autor/Desktop/auto-ring/GENERIQUES/temp/courant.abw", "w")
    g_temp.write(f)
    g_temp.close()
     
    exp = subprocess.Popen("gimp --verbose -i -d --batch-interpreter=python-fu-eval -b - < '/home/autor/Desktop/auto-ring/GENERIQUES/gen_gene_abi_029_c.py'", shell = True)
    while exp.poll() == None :
                pass

    #### compilation du mpeg
    
    f = open("/mnt/ramdisk/gene.save", "r")
    dico_element = {}
    dico_element = pickle.load(f)
    f.close() 
    
    f = open("/mnt/ramdisk/gene_liste.save", "r")
    liste_des_fichiers = []
    liste_des_fichiers = pickle.load(f)
    f.close()
    
    dico_len = {}
    
    for c in dico_element :
        
        if dico_len.has_key(str((c).split("_")[0])) :
            dico_len[str((c).split("_")[0])] = dico_len[str((c).split("_")[0])] + dico_element[c]["lenght"]
        else :
            dico_len[str((c).split("_")[0])] = dico_element[c]["lenght"]
    
    print dico_len
    
    
    images_generique = []
    
    ramdisk_content = sorted(os.listdir("/mnt/ramdisk"))
    for content in ramdisk_content :
        if content[-3:] == "png" :
            images_generique.append(content)
            
    print images_generique
       
    os.chdir("/home/autor/Desktop/auto-ring/biblio/2014")         
    
    commande_mlt = "melt generique_img_new02_169.avi out=190 colour:black out=100 -mix 50 -mixer luma noir_1024x576.tga out=50 -mix 40 -mixer luma "
    duree = 190 + 100 - 50 + 50 - 40 ### out + out - mix + out - mix 
    
    for r in range(0, len(dico_len)) :
        print r
        nom_image = images_generique[r]
        #duree_image = dico_len["%d" % (r+1)] * 3 + 90 ### trois fois trop long
        duree_image = dico_len["%d" % (r+1)] + 90
        print nom_image, duree_image
        commande_mlt += "noir_1024x576.tga out=50 /mnt/ramdisk/%s out=%d -mix 40 -mixer luma  noir_1024x576.tga out=40 -mix 40 -mixer luma " % (nom_image, duree_image)
        duree += (50 + duree_image - 40 + 40 - 40) ### out + out - mix + out - mix 
        
    
    commande_mlt += "noir_1024x576.tga out=70 colour:black out=110 -mix 60 -mixer luma -consumer avformat f=avi vcodec=huffyuv aspect=@16/9 threads=7 real_time=-1 s=1024x576> /mnt/ramdisk/out.avi"
    duree += (70 + 110 - 60 ) ### out + out + mix
   
    print commande_mlt
    print duree 
      
    prev = subprocess.Popen(commande_mlt, shell = True)
    while prev.poll() == None :
                pass
                
    print "\n\n**** encodage image [ok] ****\n\n"
    
    prev2 = subprocess.Popen("ffmpeg -y -i /mnt/ramdisk/out.avi -an -lmin 0 -lmax '21*QP2LAMBDA' -mblmin 1 -qmin 1 -qmax 7 -maxrate 8500k -b:v 6000k -s 720x576 -sws_flags lanczos -pix_fmt yuv420p -me_method epzs -bf 2 -trellis 2 -cmp 2 -subcmp 2 -f mpeg2video /mnt/ramdisk/test_mod.m2v", shell = True)
    while prev2.poll() == None :
                pass
             
    print "\n\n**** encodage mpeg image [ok] ****\n\n"
    
    mpl = subprocess.Popen("mplex -f 8 /mnt/ramdisk/test_mod.m2v -o /mnt/ramdisk/test.mpg", shell = True)
    while mpl.poll() == None :
                pass
                
    print "\n\n**** multiplexage [ok] ****\n\n"
        
    shutil.copy("/mnt/ramdisk/test.mpg", "/mnt/nfs_out/%s/generique_%s_mplex.mpg" % (dico["nom_base"], dico["nom_base"]))
                
    cop_2 = subprocess.Popen("scp /mnt/ramdisk/test.mpg root@192.168.0.82:'/datas/F/GENERIQUES/gene_%s_mplex.mpg'" % dico["nom_base"], shell = True)
    while cop_2.poll() == None :
                pass
                
    files = glob.glob('/mnt/ramdisk/*')
    for f in files:
        os.remove(f)
    
    print "\n\n**** copie dans le repertoire generique_factory [ok] ****\n\n*****          TERMINE               *******"
    
