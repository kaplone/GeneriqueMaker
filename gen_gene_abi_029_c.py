# -*- coding: utf-8 -*-

import sys
import os, os.path
import shutil
import subprocess
import pickle
import time
import codecs

sys.path.append("/home/autor/Desktop/auto-ring")
sys.path.append("/usr/lib/gimp/2.0/python")

from gimpfu import *

liste_transposition_police = ["Times New Roman", "Arial Black"]

transposition_police = {"Times New Roman" : "Times New Roman,",
                        "Arial Black" : "Arial Black,"
                        }

fich = open("/home/autor/Desktop/auto-ring/GENERIQUES/temp/courant.abw", "r")

l_fich = fich.readlines()

numero_de_page = 1
numero_de_ligne = 1
numero_d_element = 1

dico_element = {}
dico_element["defaut"] = {}
dic_layers = {}
dic_images = {}

dic_tailles = {}
historique_total_tailles = {}
hauteur_totale_elements_page = {}
largeur_totale_elements_ligne = {}
historique_total_largeur = {}
gap ={}

meme_ligne = {}

liste_des_fichiers = []

for l in l_fich :
    
    if l[:3] == "<s ":
        liste_des_defauts = l.split('" ')
        for defaut in liste_des_defauts :
            if defaut[:6] == "props=" :
                defaut = defaut[7:]
                liste_des_elements_defauts = defaut.split("; ")
                for l_element_defaut in liste_des_elements_defauts :
                    dico_element["defaut"][l_element_defaut.split(":")[0]] = l_element_defaut.split(":")[1]
                #print dico_element["defaut"]
    
    if l[:3] == "<p ":
        if "<c props=" in l:
        
            utile = l.split("<c props=")[1:]
            
            if len(utile) == 1:
                propre = utile[0].split("</c>")[:-1]
                for p in propre :
                    texte = p.split(">")[-1]
                    #print "texte : *%s*" %texte
                    if texte == "//" :
                        numero_de_page = numero_de_page + 1
                        numero_de_ligne = 0
                        numero_d_element = 0
                    else :
                        dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)] = dict(dico_element["defaut"])
                        dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]["texte"] = texte
                        dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]["lenght"] = len(texte)
                        print(len(texte))
                    
                        datas = p.split('"')[1]
                        infos = datas.split("; ")
                        for i in infos :
                            ii = i.split(":")
                            
                        ############## test pour recuperer italic + bold ######
                            if ii[1] == "normal" :
                                ii[1] = ""
                            #######################################################
                            
                            if ii[1] in liste_transposition_police :
                                ii[1] = transposition_police[ii[1]]
                                
                            dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)][str(ii[0])] = ii[1]
                            print "%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element), dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]

                        numero_d_element = numero_d_element + 1
                        
                numero_de_ligne = numero_de_ligne + 1    
                numero_d_element = 1                  
                    
            else:
                for u in utile :
                   # print "-- U :", u
                    if u[-1] == "\n" :
                        u = u[:-5]
                        
                        
                
                    propre = u.split("</c>")[:-1]
                    
                    for p in propre :
                        texte = p.split(">")[-1]
                        #print "texte : *%s*" %texte
                        if texte.strip() == "//" :
                            print "cas 2"
                            numero_de_page = numero_de_page + 1
                            numero_de_ligne = 0
                            numero_d_element = 0
                            
                        elif texte =="" :
                            print "VIDE", p
                        else :
                            dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)] = dict(dico_element["defaut"])
                            dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]["texte"] = texte
                            dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]["lenght"] = len(texte)
                        
                            datas = p.split('"')[1]
                            infos = datas.split("; ")
                            for i in infos :
                                ii = i.split(":")
                                
                                ############## test pour recuperer italic + bold ######
                                if ii[1] == "normal" :
                                    ii[1] = ""
                                #######################################################
                                
                                if ii[1] in liste_transposition_police :
                                    ii[1] = transposition_police[ii[1]]
                                    
                       ########## repartition des informations dans un dictionnaire #############             
                                    
                                dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)][str(ii[0])] = ii[1]
                                print "%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element), dico_element["%d_%d_%d" % (numero_de_page, numero_de_ligne, numero_d_element)]
                                
                            numero_d_element = numero_d_element + 1
                            
            numero_de_ligne = numero_de_ligne + 1    
            numero_d_element = 1           

marqueur_alpha = marqueur_alpha_100 = 1000
marqueur_page = 1
marqueur_layer = 1  
nb_meme_ligne = 0
x = 0

del dico_element["defaut"] ## ajout
liste_des_elements = sorted(dico_element) 
print "#############\n\n", liste_des_elements, "###############"


while x < (len(liste_des_elements)) :
    print x, liste_des_elements[x]
    
    dic_images["%d" % (marqueur_page)] = pdb.file_png_load("/home/autor/Desktop/auto-ring/biblio/2014/noir_1024x576.png", "")
    
    hauteur_totale_elements_page["%d" % (marqueur_page)] = 0
    
    while int(liste_des_elements[x].split("_")[0]) == marqueur_page :

        if dico_element[liste_des_elements[x]]["texte"].strip() == "" : ### cas d'un saut a la ligne ###
            
            try :
                hauteur_totale_elements_page["%d" % (marqueur_page)] = hauteur_totale_elements_page["%d" % (marqueur_page)] + pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer -1 )])
            except :
                hauteur_totale_elements_page["%d" % (marqueur_page)] = hauteur_totale_elements_page["%d" % (marqueur_page)] + pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer +1 )])
            meme_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = 0
            
        else :                                      
            dic_layers["%d_%d" % (marqueur_page, marqueur_layer)] = pdb.gimp_text_layer_new(dic_images["%d" % (marqueur_page)],
                                                                                            dico_element[liste_des_elements[x]]["texte"],
                                                                                           dico_element[liste_des_elements[x]]["font-family"],
                                                                                            float(dico_element[liste_des_elements[x]]["font-size"][:-2]) * 4,
                                                                                            0
                                                                                            )
                                                                                            
            dic_tailles["%d_%d" % (marqueur_page, marqueur_layer)] = pdb.gimp_drawable_width(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)]), pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)])
            
            if x > 1:
                if liste_des_elements[x].split("_")[0] != liste_des_elements[x-1].split("_")[0] :
                    historique_total_tailles["%d_%d" % (marqueur_page, marqueur_layer)] = hauteur_totale_elements_page["%d" % (marqueur_page)]
                    hauteur_totale_elements_page["%d" % (marqueur_page)] = hauteur_totale_elements_page["%d" % (marqueur_page)] + pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)])
                    meme_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = 0
                    
                else : 
                    if liste_des_elements[x].split("_")[1] != liste_des_elements[x-1].split("_")[1] :
                        historique_total_tailles["%d_%d" % (marqueur_page, marqueur_layer)] = hauteur_totale_elements_page["%d" % (marqueur_page)]
                        hauteur_totale_elements_page["%d" % (marqueur_page)] = hauteur_totale_elements_page["%d" % (marqueur_page)] + pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)])
                        meme_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = 0
                        
                    else :
                        historique_total_tailles["%d_%d" % (marqueur_page, marqueur_layer)] = hauteur_totale_elements_page["%d" % (marqueur_page)]
                        nb_meme_ligne = nb_meme_ligne +1
                        meme_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = nb_meme_ligne
                        
                        largeur_totale_elements_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = 0
                        largeur_totale_elements_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = largeur_totale_elements_ligne["%d_%d" % (marqueur_page, marqueur_layer)] + pdb.gimp_drawable_width(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)])
                                               
                        historique_total_largeur["%d_%d" % (marqueur_page, marqueur_layer)] = largeur_totale_elements_ligne["%d_%d" % (marqueur_page, marqueur_layer)]
                        
                                                                                      
            else:
                historique_total_tailles["%d_%d" % (marqueur_page, marqueur_layer)] = hauteur_totale_elements_page["%d" % (marqueur_page)]
                hauteur_totale_elements_page["%d" % (marqueur_page)] = hauteur_totale_elements_page["%d" % (marqueur_page)] + pdb.gimp_drawable_height(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)])
                meme_ligne["%d_%d" % (marqueur_page, marqueur_layer)] = 0
                
            pdb.gimp_image_add_layer(dic_images["%d" % (marqueur_page)],
                                     dic_layers["%d_%d" % (marqueur_page, marqueur_layer)],
                                     0
                                     )
                                     
            pdb.gimp_text_layer_set_color(dic_layers["%d_%d" % (marqueur_page, marqueur_layer)], (0.9,0.9,0.9,marqueur_alpha))     
                                
            marqueur_layer = marqueur_layer + 1 
                                    
        x = x +1
        print "=============", x
        if x == len(liste_des_elements) :
            break

        
    #gap["%d" % (marqueur_page)] = ((496 - hauteur_totale_elements_page["%d" % (marqueur_page)])) / (marqueur_layer + 1)  ### 40 de marge en haut et en bas  
    #gap["%d" % (marqueur_page)] = ((436 - hauteur_totale_elements_page["%d" % (marqueur_page)])) / (marqueur_layer + 1)  ### 70 de marge en haut et en bas    
    gap["%d" % (marqueur_page)] = ((356 - hauteur_totale_elements_page["%d" % (marqueur_page)])) / (marqueur_layer + 1)  ### 110 de marge en haut et en bas    
    #gap["%d" % (marqueur_page)] = ((316 - hauteur_totale_elements_page["%d" % (marqueur_page)])) / (marqueur_layer + 1)  ### 130 de marge en haut et en bas    
        
    for h in range(1, marqueur_layer + 1) :
        
        if h == 1 :


            pdb.gimp_layer_set_offsets(dic_layers["%d_%d" % (marqueur_page, h)],
                                       (1024 - pdb.gimp_drawable_width(dic_layers["%d_%d" % (marqueur_page, h)])) / 2,
                                       gap["%d" % (marqueur_page)]  + historique_total_tailles["%d_%d" % (marqueur_page, h)] + 110,
                                       )
        else :
            try :
                if meme_ligne["%d_%d" % (marqueur_page, h)] != 0 :

                    pdb.gimp_layer_set_offsets(dic_layers["%d_%d" % (marqueur_page, h)],
                                               (1024 - largeur_totale_elements_ligne["%d_%d" % (marqueur_page, h)])  / 2 + historique_total_largeur["%d_%d" % (marqueur_page, h -1 )],
                                               (h - nb_meme_ligne) * gap["%d" % (marqueur_page)] + historique_total_tailles["%d_%d" % (marqueur_page, h)] + 110 ,
                                               )
                    
                else :

                    pdb.gimp_layer_set_offsets(dic_layers["%d_%d" % (marqueur_page, h)],
                                               (1024 - pdb.gimp_drawable_width(dic_layers["%d_%d" % (marqueur_page, h)])) / 2,
                                               h * gap["%d" % (marqueur_page)] + historique_total_tailles["%d_%d" % (marqueur_page, h)] + 110,
                                               )
               
            except :
                pass    
        
    
    layer_flat = pdb.gimp_image_flatten(dic_images["%d" % (marqueur_page)])

    pdb.file_png_save_defaults(dic_images["%d" % (marqueur_page)],
                       layer_flat, 
                       "/mnt/ramdisk/u%d_%d_alpha_%03d.png" % (marqueur_page, marqueur_layer, marqueur_alpha_100), 
                       "save1_link_png"
                      )
        
    liste_des_fichiers.append("%d_%d" % (marqueur_page, marqueur_layer))
        
    marqueur_page = marqueur_page + 1
    marqueur_layer = 1


dico_save = dico_element
###f = open(dico_save["repertoire"] + "/generique.save", "w")
f = open("/mnt/ramdisk/gene.save", "w")
pickle.dump(dico_save, f)
f.close()


###f = open(dico_save["repertoire"] + "/generique.save", "w")
f = open("/mnt/ramdisk/gene_liste.save", "w")
pickle.dump(liste_des_fichiers, f)
f.close()
    
pdb.gimp_quit(0)



