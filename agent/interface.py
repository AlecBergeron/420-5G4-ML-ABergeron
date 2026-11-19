from __future__ import annotations

import sys
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

DOSSIER_AGENT = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER_AGENT / "build"))

import bibliotheque_py


COULEURS = {
    "page": "#9E9E9E",
    "barre": "#4A4A4A",
    "onglet_actif": "#A6A6A6",
    "onglet_survol": "#5C5C5C",
    "cadre": "#D2D2D2",
    "panneau": "#FFFFFF",
    "bordure": "#1A1A1A",
    "bouton": "#FFFFFF",
    "bouton_survol": "#F0F0F0",
    "texte": "#111111",
    "texte_navigation": "#F2F2F2",
    "quitter": "#C00000",
    "selection": "#D9D9D9",
    "erreur": "#B00020",
    "texte_desactive": "#777777",
}

ONGLETS = (
    ("livres", "Livres"),
    ("users", "Users"),
    ("sauvegarde", "Sauvegarde"),
)


def creer_bouton_action(parent, texte, commande, **kwargs):
    options = {
        "width": 150,
        "height": 44,
        "corner_radius": 8,
        "border_width": 1,
        "border_color": COULEURS["bordure"],
        "fg_color": COULEURS["bouton"],
        "hover_color": COULEURS["bouton_survol"],
        "text_color": COULEURS["texte"],
        "font": ("Helvetica", 18),
    }
    options.update(kwargs)
    return ctk.CTkButton(parent, text=texte, command=commande, **options)


class ComboAvecContour(ctk.CTkComboBox):
    def _dessiner_contour_fleche(self):
        largeur = self._apply_widget_scaling(self._current_width)
        hauteur = self._apply_widget_scaling(self._current_height)
        decoupe = largeur - hauteur

        if self._canvas.find_withtag("contour_fleche"):
            self._canvas.coords("contour_fleche", decoupe, 0, decoupe, hauteur)
        else:
            self._canvas.create_line(
                decoupe,
                0,
                decoupe,
                hauteur,
                fill=COULEURS["bordure"],
                width=1,
                tags=("contour_fleche",),
            )
        self._canvas.tag_raise("contour_fleche")

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        self._dessiner_contour_fleche()


class FenetreModale(ctk.CTkToplevel):
    def __init__(self, parent, titre, largeur=640, hauteur=520, texte_valider="Ajouter"):
        super().__init__(parent)
        self.parent = parent
        self.withdraw()
        self.title(titre)
        self.configure(fg_color=COULEURS["cadre"])
        self.resizable(False, False)
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.fermer)
        self.bind("<Escape>", lambda _: self.fermer())
        self.bind("<Return>", lambda _: self.valider())

        carte = ctk.CTkFrame(
            self,
            fg_color=COULEURS["panneau"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=36,
        )
        carte.pack(fill="both", expand=True, padx=1, pady=1)
        carte.grid_columnconfigure(0, weight=1)
        carte.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            carte,
            text=titre,
            text_color=COULEURS["texte"],
            font=("Helvetica", 24),
        ).grid(row=0, column=0, pady=(20, 12))

        self.panneau_formulaire = ctk.CTkFrame(
            carte,
            fg_color=COULEURS["panneau"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=0,
        )
        self.panneau_formulaire.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 10))
        self.panneau_formulaire.grid_columnconfigure(1, weight=1)

        pied = ctk.CTkFrame(carte, fg_color="transparent", corner_radius=0)
        pied.grid(row=2, column=0, sticky="ew", padx=28, pady=(0, 20))
        pied.grid_columnconfigure(0, weight=1)
        pied.grid_columnconfigure(1, weight=0)

        self.label_erreur = ctk.CTkLabel(
            pied,
            text="",
            anchor="w",
            text_color=COULEURS["erreur"],
            font=("Helvetica", 14),
        )
        self.label_erreur.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self.bouton_annuler = creer_bouton_action(
            pied,
            "Annuler",
            self.fermer,
            width=140,
            height=42,
        )
        self.bouton_annuler.grid(row=1, column=0, sticky="e", padx=(0, 10))

        self.bouton_valider = creer_bouton_action(
            pied,
            texte_valider,
            self.valider,
            width=140,
            height=42,
        )
        self.bouton_valider.grid(row=1, column=1, sticky="e")

        self.centrer(largeur, hauteur)
        self.deiconify()
        self.update_idletasks()
        self.grab_set()
        self.focus_force()

    def centrer(self, largeur, hauteur):
        self.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - largeur) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - hauteur) // 2
        self.geometry(f"{largeur}x{hauteur}+{max(x, 0)}+{max(y, 0)}")

    def afficher_erreur(self, message):
        self.label_erreur.configure(text=message)

    def effacer_erreur(self):
        self.label_erreur.configure(text="")

    def ajouter_champ(self, ligne, libelle, variable):
        ctk.CTkLabel(
            self.panneau_formulaire,
            text=libelle,
            anchor="w",
            text_color=COULEURS["texte"],
            font=("Helvetica", 20),
        ).grid(row=ligne, column=0, sticky="w", padx=(24, 16), pady=(18, 0))

        entree = ctk.CTkEntry(
            self.panneau_formulaire,
            textvariable=variable,
            height=38,
            corner_radius=0,
            border_width=1,
            border_color=COULEURS["bordure"],
            fg_color=COULEURS["panneau"],
            text_color=COULEURS["texte"],
            font=("Helvetica", 18),
        )
        entree.grid(row=ligne, column=1, sticky="ew", padx=(0, 24), pady=(18, 0))
        return entree

    def valider(self):
        pass

    def fermer(self):
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()


class ModalAjouterLivre(FenetreModale):
    def __init__(self, parent, bibliotheque, on_ajout=None):
        super().__init__(parent, "Ajouter un livre", largeur=640, hauteur=540)
        self.bibliotheque = bibliotheque
        self.on_ajout = on_ajout
        self.titre = ctk.StringVar()
        self.auteur = ctk.StringVar()
        self.isbn = ctk.StringVar()

        self.entree_titre = self.ajouter_champ(0, "Titre :", self.titre)
        self.entree_auteur = self.ajouter_champ(1, "Auteur :", self.auteur)
        self.entree_isbn = self.ajouter_champ(2, "ISBN :", self.isbn)
        self.entree_titre.focus_set()

    def valider(self):
        self.effacer_erreur()
        titre = self.titre.get().strip()
        auteur = self.auteur.get().strip()
        isbn = self.isbn.get().strip()

        if not titre or not auteur or not isbn:
            self.afficher_erreur("Tous les champs sont obligatoires.")
            return

        if self.bibliotheque.find_book_by_isbn(isbn) is not None:
            self.afficher_erreur("Un livre avec cet ISBN existe déjà.")
            return

        self.bibliotheque.add_book(bibliotheque_py.Book(titre, auteur, isbn))
        if self.on_ajout is not None:
            self.on_ajout()
        self.fermer()


class ModalAjouterUtilisateur(FenetreModale):
    def __init__(self, parent, bibliotheque, on_ajout=None):
        super().__init__(parent, "Ajouter un utilisateur", largeur=640, hauteur=480)
        self.bibliotheque = bibliotheque
        self.on_ajout = on_ajout
        self.nom = ctk.StringVar()
        self.identifiant = ctk.StringVar()

        self.entree_nom = self.ajouter_champ(0, "Nom :", self.nom)
        self.entree_identifiant = self.ajouter_champ(
            1, "Identifiant :", self.identifiant
        )
        self.entree_nom.focus_set()

    def valider(self):
        self.effacer_erreur()
        nom = self.nom.get().strip()
        identifiant = self.identifiant.get().strip()

        if not nom or not identifiant:
            self.afficher_erreur("Tous les champs sont obligatoires.")
            return

        if self.bibliotheque.find_user_by_id(identifiant) is not None:
            self.afficher_erreur("Un utilisateur avec cet identifiant existe déjà.")
            return

        self.bibliotheque.add_user(bibliotheque_py.User(nom, identifiant))
        if self.on_ajout is not None:
            self.on_ajout()
        self.fermer()


class ModalSelection(FenetreModale):
    def __init__(self, parent, titre, elements, formateur, filtre, on_choix):
        self.elements = list(elements)
        self.formateur = formateur
        self.filtre = filtre
        self.on_choix = on_choix
        self.element_selectionne = None
        self.lignes = {}
        self.elements_affiches = []

        super().__init__(
            parent,
            titre,
            largeur=640,
            hauteur=560,
            texte_valider="Choisir",
        )

        self.panneau_formulaire.grid_columnconfigure(0, weight=1)
        self.panneau_formulaire.grid_columnconfigure(1, weight=0)
        self.panneau_formulaire.grid_rowconfigure(2, weight=1)

        self.recherche = ctk.StringVar()
        self.entree_recherche = ctk.CTkEntry(
            self.panneau_formulaire,
            textvariable=self.recherche,
            placeholder_text="Rechercher",
            height=52,
            corner_radius=0,
            border_width=0,
            fg_color=COULEURS["panneau"],
            text_color=COULEURS["texte"],
            placeholder_text_color="#555555",
            font=("Helvetica", 20),
        )
        self.entree_recherche.grid(row=0, column=0, sticky="ew", padx=24, pady=10)

        separateur = ctk.CTkFrame(
            self.panneau_formulaire,
            height=1,
            fg_color=COULEURS["bordure"],
            corner_radius=0,
        )
        separateur.grid(row=1, column=0, sticky="ew")

        self.liste = ctk.CTkScrollableFrame(
            self.panneau_formulaire,
            fg_color=COULEURS["panneau"],
            corner_radius=0,
            border_width=1,
            border_color=COULEURS["bordure"],
            label_text="",
        )
        self.liste.grid(row=2, column=0, sticky="nsew", padx=12, pady=(10, 12))

        self.recherche.trace_add("write", self.actualiser_liste)
        self.actualiser_liste()
        self.entree_recherche.focus_set()

    def actualiser_liste(self, *_):
        self.element_selectionne = None
        self.lignes = {}
        self.effacer_erreur()

        for widget in self.liste.winfo_children():
            widget.destroy()

        requete = self.recherche.get().strip()
        self.elements_affiches = [
            element
            for element in self.elements
            if not requete or self.filtre(element, requete)
        ]

        if not self.elements_affiches:
            ctk.CTkLabel(
                self.liste,
                text="Aucun résultat",
                anchor="w",
                text_color="#666666",
                font=("Helvetica", 16),
            ).pack(fill="x", padx=24, pady=12)
            return

        for index, element in enumerate(self.elements_affiches):
            ligne = ctk.CTkLabel(
                self.liste,
                text=self.formateur(element),
                anchor="w",
                justify="left",
                height=34,
                fg_color="transparent",
                text_color=COULEURS["texte"],
                font=("Helvetica", 16),
                cursor="hand2",
            )
            ligne.pack(fill="x", padx=24)
            ligne.bind("<Button-1>", lambda _, i=index: self.selectionner(i))
            self.lignes[index] = ligne

    def selectionner(self, index):
        self.element_selectionne = index
        self.effacer_erreur()

        for autre_index, ligne in self.lignes.items():
            ligne.configure(
                fg_color=COULEURS["selection"]
                if autre_index == index
                else "transparent"
            )

    def valider(self):
        if self.element_selectionne is None:
            self.afficher_erreur("Veuillez sélectionner un élément.")
            return

        element = self.elements_affiches[self.element_selectionne]
        self.fermer()
        self.on_choix(element)


def formater_utilisateur(utilisateur):
    nombre = utilisateur.borrowed_book_count()
    if nombre == 0:
        etat = "n'a pas d'emprunt"
    elif nombre == 1:
        etat = "a un emprunt"
    else:
        etat = f"a {nombre} emprunts"
    return f"{utilisateur.name}, {utilisateur.user_id}, {etat}"


class ModalChoisirLivre(ModalSelection):
    def __init__(self, parent, livres, on_choix):
        super().__init__(
            parent,
            "Choisir un livre",
            livres,
            formateur=lambda livre: f"{livre.title}, {livre.author}, {livre.isbn}",
            filtre=lambda livre, requete: requete.casefold()
            in f"{livre.title} {livre.author} {livre.isbn}".casefold(),
            on_choix=on_choix,
        )


class ModalChoisirUtilisateur(ModalSelection):
    def __init__(self, parent, utilisateurs, on_choix):
        super().__init__(
            parent,
            "Choisir un utilisateur",
            utilisateurs,
            formateur=formater_utilisateur,
            filtre=lambda utilisateur, requete: requete.casefold()
            in f"{utilisateur.name} {utilisateur.user_id}".casefold(),
            on_choix=on_choix,
        )


class BarreNavigation(ctk.CTkFrame):
    def __init__(self, parent, commande, **kwargs):
        super().__init__(
            parent,
            fg_color=COULEURS["barre"],
            corner_radius=0,
            height=127,
            **kwargs,
        )
        self.grid_propagate(False)
        self.command = commande
        self.boutons = {}

        conteneur = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        conteneur.pack(side="bottom", anchor="w", padx=30)

        for cle, libelle in ONGLETS:
            bouton = ctk.CTkButton(
                conteneur,
                text=libelle,
                width=227,
                height=78,
                corner_radius=0,
                border_width=0,
                fg_color="transparent",
                hover_color=COULEURS["onglet_survol"],
                text_color=COULEURS["texte_navigation"],
                font=("Helvetica", 24),
                command=lambda nom=cle: self.command(nom),
            )
            bouton.pack(side="left", padx=(0, 16))
            self.boutons[cle] = bouton

    def set_actif(self, cle_active):
        for cle, bouton in self.boutons.items():
            actif = cle == cle_active
            bouton.configure(
                fg_color=COULEURS["onglet_actif"] if actif else "transparent",
                hover_color=COULEURS["onglet_actif"] if actif else COULEURS["onglet_survol"],
            )


class PagePrincipale(ctk.CTkFrame):
    def __init__(self, parent, commande_quitter, **kwargs):
        super().__init__(parent, fg_color=COULEURS["page"], corner_radius=0, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        cadre = ctk.CTkFrame(
            self,
            fg_color=COULEURS["cadre"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=0,
        )
        cadre.grid(row=0, column=0, sticky="nsew", padx=30, pady=24)
        cadre.grid_rowconfigure(0, weight=1)
        cadre.grid_columnconfigure(0, weight=1)
        cadre.grid_columnconfigure(1, minsize=200)

        self.panneau_contenu = ctk.CTkFrame(
            cadre,
            fg_color=COULEURS["panneau"],
            border_width=1,
            border_color=COULEURS["bordure"],
            corner_radius=0,
        )
        self.panneau_contenu.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 16),
            pady=20,
        )

        self.panneau_actions = ctk.CTkFrame(
            cadre,
            fg_color="transparent",
            corner_radius=0,
        )
        self.panneau_actions.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 30),
            pady=20,
        )
        self.panneau_actions.grid_rowconfigure(0, weight=1)
        self.panneau_actions.grid_columnconfigure(0, weight=1)

        self.zone_actions = ctk.CTkFrame(
            self.panneau_actions,
            fg_color="transparent",
            corner_radius=0,
        )
        self.zone_actions.grid(row=0, column=0, sticky="new")
        self.zone_actions.grid_columnconfigure(0, weight=1)

        self.bouton_quitter = ctk.CTkButton(
            self.panneau_actions,
            text="Quitter",
            width=150,
            height=44,
            corner_radius=8,
            border_width=1,
            border_color=COULEURS["bordure"],
            fg_color=COULEURS["bouton"],
            hover_color=COULEURS["bouton_survol"],
            text_color=COULEURS["quitter"],
            font=("Helvetica", 18),
            command=commande_quitter,
        )
        self.bouton_quitter.grid(row=1, column=0, sticky="e")


class PageLivres(PagePrincipale):
    def __init__(self, parent, commande_quitter, bibliotheque, **kwargs):
        super().__init__(parent, commande_quitter, **kwargs)
        self.bibliotheque = bibliotheque
        self.recherche = ctk.StringVar()
        self.mode_recherche = ctk.StringVar(value="Titre")
        self.disponibles_seulement = ctk.IntVar(value=0)
        self.livre_selectionne = None
        self.lignes_livres = {}

        self.combo_mode = ComboAvecContour(
            self.zone_actions,
            values=["Titre", "Auteur"],
            variable=self.mode_recherche,
            state="readonly",
            width=150,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=COULEURS["bordure"],
            fg_color=COULEURS["bouton"],
            button_color=COULEURS["bouton"],
            button_hover_color=COULEURS["bouton_survol"],
            dropdown_fg_color=COULEURS["bouton"],
            dropdown_hover_color=COULEURS["bouton_survol"],
            dropdown_text_color=COULEURS["texte"],
            text_color=COULEURS["texte"],
            font=("Helvetica", 18),
            dropdown_font=("Helvetica", 16),
            command=self.actualiser_liste,
        )
        self.combo_mode.grid(row=0, column=0, sticky="e")

        self.filtre_disponibles = ctk.CTkSwitch(
            self.zone_actions,
            text="Disponible",
            variable=self.disponibles_seulement,
            onvalue=1,
            offvalue=0,
            command=self.actualiser_liste,
            width=150,
            height=28,
            switch_width=40,
            switch_height=22,
            corner_radius=11,
            border_width=1,
            border_color=COULEURS["bordure"],
            fg_color="#D9D9D9",
            progress_color=COULEURS["barre"],
            button_color=COULEURS["panneau"],
            button_hover_color=COULEURS["bouton_survol"],
            text_color=COULEURS["texte"],
            font=("Helvetica", 16),
        )
        self.filtre_disponibles.grid(row=1, column=0, sticky="e", pady=(18, 0))

        self.bouton_ajouter = creer_bouton_action(
            self.zone_actions,
            "Ajouter",
            self.ouvrir_modal_ajout,
        )
        self.bouton_ajouter.grid(row=2, column=0, sticky="e", pady=(18, 0))

        self.bouton_supprimer = creer_bouton_action(
            self.zone_actions,
            "Supprimer",
            self.supprimer_livre,
            state="disabled",
            text_color_disabled=COULEURS["texte_desactive"],
        )
        self.bouton_supprimer.grid(row=3, column=0, sticky="e", pady=(12, 0))

        self.bouton_emprunter = creer_bouton_action(
            self.zone_actions,
            "Emprunter",
            self.ouvrir_modal_emprunt,
        )
        self.bouton_emprunter.grid(row=4, column=0, sticky="e", pady=(12, 0))

        self.bouton_retourner = creer_bouton_action(
            self.zone_actions,
            "Retourner",
            self.ouvrir_modal_retour,
        )
        self.bouton_retourner.grid(row=5, column=0, sticky="e", pady=(12, 0))

        self.panneau_contenu.grid_rowconfigure(0, weight=0)
        self.panneau_contenu.grid_rowconfigure(1, weight=0)
        self.panneau_contenu.grid_rowconfigure(2, weight=1)
        self.panneau_contenu.grid_rowconfigure(3, weight=0)
        self.panneau_contenu.grid_columnconfigure(0, weight=1)

        self.entree_recherche = ctk.CTkEntry(
            self.panneau_contenu,
            textvariable=self.recherche,
            placeholder_text="Rechercher",
            height=54,
            corner_radius=0,
            border_width=0,
            fg_color=COULEURS["panneau"],
            text_color=COULEURS["texte"],
            placeholder_text_color="#555555",
            font=("Helvetica", 20),
        )
        self.entree_recherche.grid(row=0, column=0, sticky="ew", padx=24, pady=10)

        separateur = ctk.CTkFrame(
            self.panneau_contenu,
            height=1,
            fg_color=COULEURS["bordure"],
            corner_radius=0,
        )
        separateur.grid(row=1, column=0, sticky="ew", padx=(1, 1))

        self.liste_livres = ctk.CTkScrollableFrame(
            self.panneau_contenu,
            fg_color=COULEURS["panneau"],
            corner_radius=0,
            border_width=0,
            label_text="",
        )
        self.liste_livres.grid(row=2, column=0, sticky="nsew", padx=(1, 1))

        ligne_bas = ctk.CTkFrame(
            self.panneau_contenu,
            height=1,
            fg_color=COULEURS["bordure"],
            corner_radius=0,
        )
        ligne_bas.grid(row=3, column=0, sticky="ew", padx=(1, 1))

        self.recherche.trace_add("write", self.actualiser_liste)
        self.mode_recherche.trace_add("write", self.actualiser_liste)
        self.actualiser_liste()

    def actualiser_liste(self, *_):
        self.livre_selectionne = None
        self.lignes_livres = {}
        self.bouton_supprimer.configure(state="disabled")

        for widget in self.liste_livres.winfo_children():
            widget.destroy()

        recherche = self.recherche.get().strip()
        if recherche and self.mode_recherche.get() == "Auteur":
            livres = self.bibliotheque.search_books_by_author(recherche)
        elif recherche:
            livres = self.bibliotheque.search_books_by_title(recherche)
        else:
            livres = self.bibliotheque.get_all_books()

        if self.disponibles_seulement.get():
            livres = [livre for livre in livres if livre.is_available]

        if not livres:
            ctk.CTkLabel(
                self.liste_livres,
                text="Aucun livre trouvé",
                anchor="w",
                text_color="#666666",
                font=("Helvetica", 16),
            ).pack(fill="x", padx=24, pady=12)
            return

        for livre in livres:
            ligne = ctk.CTkLabel(
                self.liste_livres,
                text=f"{livre.title}, {livre.author}, {livre.isbn}",
                anchor="w",
                justify="left",
                height=34,
                fg_color="transparent",
                text_color=COULEURS["texte"],
                font=("Helvetica", 16),
                cursor="hand2",
            )
            ligne.pack(fill="x", padx=24, pady=0)
            ligne.bind(
                "<Button-1>",
                lambda _, isbn=livre.isbn: self.selectionner_livre(isbn),
            )
            self.lignes_livres[livre.isbn] = ligne

    def selectionner_livre(self, isbn):
        self.livre_selectionne = isbn
        for autre_isbn, ligne in self.lignes_livres.items():
            ligne.configure(
                fg_color=COULEURS["selection"] if autre_isbn == isbn else "transparent"
            )
        self.bouton_supprimer.configure(state="normal")

    def ouvrir_modal_ajout(self):
        ModalAjouterLivre(
            self.winfo_toplevel(),
            self.bibliotheque,
            self.actualiser_liste,
        )

    def ouvrir_modal_emprunt(self):
        ModalChoisirLivre(
            self.winfo_toplevel(),
            self.bibliotheque.get_available_books(),
            self._choisir_utilisateur_pour_emprunt,
        )

    def _choisir_utilisateur_pour_emprunt(self, livre):
        ModalChoisirUtilisateur(
            self.winfo_toplevel(),
            self.bibliotheque.get_all_users(),
            lambda utilisateur: self.emprunter_livre(livre.isbn, utilisateur.user_id),
        )

    def emprunter_livre(self, isbn, user_id):
        if not self.bibliotheque.check_out_book(isbn, user_id):
            messagebox.showerror(
                "Emprunt impossible",
                "Impossible d'emprunter ce livre.",
                parent=self.winfo_toplevel(),
            )
            return
        self.actualiser_liste()

    def ouvrir_modal_retour(self):
        livres = [
            livre
            for livre in self.bibliotheque.get_all_books()
            if not livre.is_available
        ]
        ModalChoisirLivre(
            self.winfo_toplevel(),
            livres,
            self.retourner_livre,
        )

    def retourner_livre(self, livre):
        if not self.bibliotheque.return_book(livre.isbn):
            messagebox.showerror(
                "Retour impossible",
                "Impossible de retourner ce livre.",
                parent=self.winfo_toplevel(),
            )
            return
        self.actualiser_liste()

    def supprimer_livre(self):
        isbn = self.livre_selectionne
        if isbn is None:
            return

        livre = self.bibliotheque.find_book_by_isbn(isbn)
        if livre is None:
            self.actualiser_liste()
            return

        if not livre.is_available:
            messagebox.showerror(
                "Suppression impossible",
                "Ce livre est actuellement emprunté et ne peut pas être supprimé.",
                parent=self.winfo_toplevel(),
            )
            return

        if not self.bibliotheque.remove_book(isbn):
            messagebox.showerror(
                "Suppression impossible",
                "Impossible de supprimer ce livre.",
                parent=self.winfo_toplevel(),
            )
            return

        self.actualiser_liste()


class PageUsers(PagePrincipale):
    def __init__(self, parent, commande_quitter, bibliotheque, **kwargs):
        super().__init__(parent, commande_quitter, **kwargs)
        self.bibliotheque = bibliotheque
        self.recherche = ctk.StringVar()
        self.utilisateur_selectionne = None
        self.lignes_users = {}

        self.bouton_ajouter = creer_bouton_action(
            self.zone_actions,
            "Ajouter",
            self.ouvrir_modal_ajout,
        )
        self.bouton_ajouter.grid(row=0, column=0, sticky="e")

        self.bouton_supprimer = creer_bouton_action(
            self.zone_actions,
            "Supprimer",
            self.supprimer_utilisateur,
            state="disabled",
            text_color_disabled=COULEURS["texte_desactive"],
        )
        self.bouton_supprimer.grid(row=1, column=0, sticky="e", pady=(12, 0))

        self.bouton_emprunter = creer_bouton_action(
            self.zone_actions,
            "Emprunter",
            self.ouvrir_modal_emprunt,
        )
        self.bouton_emprunter.grid(row=2, column=0, sticky="e", pady=(12, 0))

        self.bouton_retourner = creer_bouton_action(
            self.zone_actions,
            "Retourner",
            self.ouvrir_modal_retour,
        )
        self.bouton_retourner.grid(row=3, column=0, sticky="e", pady=(12, 0))

        self.panneau_contenu.grid_rowconfigure(0, weight=0)
        self.panneau_contenu.grid_rowconfigure(1, weight=0)
        self.panneau_contenu.grid_rowconfigure(2, weight=1)
        self.panneau_contenu.grid_rowconfigure(3, weight=0)
        self.panneau_contenu.grid_columnconfigure(0, weight=1)

        self.entree_recherche = ctk.CTkEntry(
            self.panneau_contenu,
            textvariable=self.recherche,
            placeholder_text="Rechercher",
            height=54,
            corner_radius=0,
            border_width=0,
            fg_color=COULEURS["panneau"],
            text_color=COULEURS["texte"],
            placeholder_text_color="#555555",
            font=("Helvetica", 20),
        )
        self.entree_recherche.grid(row=0, column=0, sticky="ew", padx=24, pady=10)

        separateur = ctk.CTkFrame(
            self.panneau_contenu,
            height=1,
            fg_color=COULEURS["bordure"],
            corner_radius=0,
        )
        separateur.grid(row=1, column=0, sticky="ew", padx=(1, 1))

        self.liste_users = ctk.CTkScrollableFrame(
            self.panneau_contenu,
            fg_color=COULEURS["panneau"],
            corner_radius=0,
            border_width=0,
            label_text="",
        )
        self.liste_users.grid(row=2, column=0, sticky="nsew", padx=(1, 1))

        ligne_bas = ctk.CTkFrame(
            self.panneau_contenu,
            height=1,
            fg_color=COULEURS["bordure"],
            corner_radius=0,
        )
        ligne_bas.grid(row=3, column=0, sticky="ew", padx=(1, 1))

        self.recherche.trace_add("write", self.actualiser_liste)
        self.actualiser_liste()

    def actualiser_liste(self, *_):
        self.utilisateur_selectionne = None
        self.lignes_users = {}
        self.bouton_supprimer.configure(state="disabled")

        for widget in self.liste_users.winfo_children():
            widget.destroy()

        utilisateurs = self.bibliotheque.get_all_users()
        recherche = self.recherche.get().strip()
        if recherche:
            requete = recherche.casefold()
            utilisateurs = [
                utilisateur
                for utilisateur in utilisateurs
                if requete in utilisateur.name.casefold()
                or requete in utilisateur.user_id.casefold()
            ]

        if not utilisateurs:
            ctk.CTkLabel(
                self.liste_users,
                text="Aucun utilisateur trouvé",
                anchor="w",
                text_color="#666666",
                font=("Helvetica", 16),
            ).pack(fill="x", padx=24, pady=12)
            return

        for utilisateur in utilisateurs:
            ligne = ctk.CTkLabel(
                self.liste_users,
                text=formater_utilisateur(utilisateur),
                anchor="w",
                justify="left",
                height=34,
                fg_color="transparent",
                text_color=COULEURS["texte"],
                font=("Helvetica", 16),
                cursor="hand2",
            )
            ligne.pack(fill="x", padx=24, pady=0)
            ligne.bind(
                "<Button-1>",
                lambda _, user_id=utilisateur.user_id: self.selectionner_utilisateur(
                    user_id
                ),
            )
            self.lignes_users[utilisateur.user_id] = ligne

    def selectionner_utilisateur(self, user_id):
        self.utilisateur_selectionne = user_id
        for autre_id, ligne in self.lignes_users.items():
            ligne.configure(
                fg_color=COULEURS["selection"]
                if autre_id == user_id
                else "transparent"
            )
        self.bouton_supprimer.configure(state="normal")

    def ouvrir_modal_ajout(self):
        ModalAjouterUtilisateur(
            self.winfo_toplevel(),
            self.bibliotheque,
            self.actualiser_liste,
        )

    def supprimer_utilisateur(self):
        user_id = self.utilisateur_selectionne
        if user_id is None:
            return

        utilisateur = self.bibliotheque.find_user_by_id(user_id)
        if utilisateur is None:
            self.actualiser_liste()
            return

        if utilisateur.borrowed_book_count() > 0:
            messagebox.showerror(
                "Suppression impossible",
                "Cet utilisateur a des emprunts en cours et ne peut pas être supprimé.",
                parent=self.winfo_toplevel(),
            )
            return

        if not self.bibliotheque.remove_user(user_id):
            messagebox.showerror(
                "Suppression impossible",
                "Impossible de supprimer cet utilisateur.",
                parent=self.winfo_toplevel(),
            )
            return

        self.actualiser_liste()

    def ouvrir_modal_emprunt(self):
        ModalChoisirUtilisateur(
            self.winfo_toplevel(),
            self.bibliotheque.get_all_users(),
            self._choisir_livre_pour_emprunt,
        )

    def _choisir_livre_pour_emprunt(self, utilisateur):
        ModalChoisirLivre(
            self.winfo_toplevel(),
            self.bibliotheque.get_available_books(),
            lambda livre: self.emprunter_livre(livre.isbn, utilisateur.user_id),
        )

    def emprunter_livre(self, isbn, user_id):
        if not self.bibliotheque.check_out_book(isbn, user_id):
            messagebox.showerror(
                "Emprunt impossible",
                "Impossible d'emprunter ce livre.",
                parent=self.winfo_toplevel(),
            )
            return
        self.actualiser_liste()

    def ouvrir_modal_retour(self):
        ModalChoisirUtilisateur(
            self.winfo_toplevel(),
            self.bibliotheque.get_all_users(),
            self._choisir_livre_pour_retour,
        )

    def _choisir_livre_pour_retour(self, utilisateur):
        livres = []
        for isbn in utilisateur.borrowed_books:
            livre = self.bibliotheque.find_book_by_isbn(isbn)
            if livre is not None and not livre.is_available:
                livres.append(livre)

        ModalChoisirLivre(
            self.winfo_toplevel(),
            livres,
            self.retourner_livre,
        )

    def retourner_livre(self, livre):
        if not self.bibliotheque.return_book(livre.isbn):
            messagebox.showerror(
                "Retour impossible",
                "Impossible de retourner ce livre.",
                parent=self.winfo_toplevel(),
            )
            return
        self.actualiser_liste()


class PageSauvegarde(PagePrincipale):
    pass


class ApplicationBibliotheque(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("Bibliothèque")
        self.geometry("1120x840")
        self.minsize(900, 680)
        self.configure(fg_color=COULEURS["page"])

        self.grid_rowconfigure(0, minsize=127)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.navigation = BarreNavigation(self, self.afficher_page)
        self.navigation.grid(row=0, column=0, sticky="nsew")

        self.conteneur = ctk.CTkFrame(
            self,
            fg_color=COULEURS["page"],
            corner_radius=0,
        )
        self.conteneur.grid(row=1, column=0, sticky="nsew")
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)

        self.bibliotheque = bibliotheque_py.Library()
        self.gestionnaire_fichiers = bibliotheque_py.FileManager(
            str(DOSSIER_AGENT / "data" / "books.txt"),
            str(DOSSIER_AGENT / "data" / "users.txt"),
        )
        self.gestionnaire_fichiers.load_library_data(self.bibliotheque)

        self.pages = {
            "livres": PageLivres(self.conteneur, self.quitter, self.bibliotheque),
            "users": PageUsers(self.conteneur, self.quitter, self.bibliotheque),
            "sauvegarde": PageSauvegarde(self.conteneur, self.quitter),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self.afficher_page("livres")
        self.protocol("WM_DELETE_WINDOW", self.quitter)

    def afficher_page(self, cle):
        self.pages[cle].tkraise()
        self.navigation.set_actif(cle)

    def quitter(self):
        try:
            self.gestionnaire_fichiers.save_library_data(self.bibliotheque)
        except Exception as erreur:
            messagebox.showerror(
                "Erreur d'enregistrement",
                str(erreur),
                parent=self,
            )
            return
        self.destroy()


if __name__ == "__main__":
    application = ApplicationBibliotheque()
    application.mainloop()
