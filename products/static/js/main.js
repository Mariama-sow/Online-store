document.addEventListener('DOMContentLoaded', function() {
    // Gestion des boutons quantité
    const decreaseBtn = document.getElementById('decrease-quantity');
    const increaseBtn = document.getElementById('increase-quantity');
    const quantityInput = document.getElementById('quantity');
    
    if (decreaseBtn && increaseBtn && quantityInput) {
        decreaseBtn.addEventListener('click', function() {
            if (quantityInput.value > 1) {
                quantityInput.value = parseInt(quantityInput.value) - 1;
            }
        });
        
        increaseBtn.addEventListener('click', function() {
            if (quantityInput.value < 10) {
                quantityInput.value = parseInt(quantityInput.value) + 1;
            }
        });
    }
    
    // Sélectionner tous les labels d'étoiles
    const starLabels = document.querySelectorAll('.star-rating-input label');
    
    // Ajouter un écouteur d'événements pour chaque label
    starLabels.forEach(label => {
        label.addEventListener('click', function() {
            // Récupérer l'ID de l'input associé
            const inputId = this.getAttribute('for');
            const starNumber = inputId.replace('star', '');
            
            // Mettre à jour visuellement les étoiles
            starLabels.forEach((lab, index) => {
                const i = lab.querySelector('i');
                if (index < starNumber) {
                    i.className = 'fas fa-star'; // Étoile pleine
                } else {
                    i.className = 'far fa-star'; // Étoile vide
                }
            });
            
            // Sélectionner le radio button correspondant
            document.getElementById(inputId).checked = true;
        });
        
        // Ajouter un effet de survol
        label.addEventListener('mouseenter', function() {
            const inputId = this.getAttribute('for');
            const starNumber = inputId.replace('star', '');
            
            starLabels.forEach((lab, index) => {
                const i = lab.querySelector('i');
                if (index < starNumber) {
                    i.className = 'fas fa-star';
                }
            });
        });
        
        label.addEventListener('mouseleave', function() {
            // Restaurer l'état sélectionné
            starLabels.forEach((lab, index) => {
                const i = lab.querySelector('i');
                const input = document.getElementById(lab.getAttribute('for'));
                if (input.checked) {
                    const checkedIndex = parseInt(input.value);
                    if (index < checkedIndex) {
                        i.className = 'fas fa-star';
                    } else {
                        i.className = 'far fa-star';
                    }
                } else {
                    i.className = 'far fa-star';
                }
            });
        });
    });
    
    // Gestion de la soumission du formulaire
    const reviewForm = document.querySelector('form[action*="add_review"]');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            // Vérifier si une note a été sélectionnée
            const ratingSelected = document.querySelector('input[name="rating"]:checked');
            if (!ratingSelected) {
                e.preventDefault();
                alert('Veuillez sélectionner une note.');
                return false;
            }
            
            // Vérifier si un commentaire a été saisi
            const comment = document.getElementById('comment').value.trim();
            if (!comment) {
                e.preventDefault();
                alert('Veuillez saisir un commentaire.');
                return false;
            }
        });
    }
    
    // Gestion des méthodes de paiement
    const paymentToggles = document.querySelectorAll('.payment-toggle');
    const paymentOptions = document.querySelectorAll('.payment-option');
    
    // Fonction pour afficher l'option de paiement sélectionnée
    function showPaymentOption(paymentMethod) {
        paymentOptions.forEach(option => {
            option.classList.remove('active');
        });
        
        const selectedOption = document.getElementById(paymentMethod + '-payment');
        if (selectedOption) {
            selectedOption.classList.add('active');
        }
    }
    
    // Écouteurs d'événements pour les boutons radio des méthodes de paiement
    paymentToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            showPaymentOption(this.value);
        });
    });
    
    // PayPal Button Handler
    const paypalButton = document.getElementById('paypal-button');
    if (paypalButton) {
        paypalButton.addEventListener('click', function() {
            const paypalModal = new bootstrap.Modal(document.getElementById('paypalModal'));
            paypalModal.show();
        });
    }
    
    // Orange Money Button Handler
    const orangeMoneyButton = document.getElementById('orange-money-button');
    if (orangeMoneyButton) {
        orangeMoneyButton.addEventListener('click', function() {
            const phoneNumberInput = document.getElementById('phone_number');
            const displayedPhone = document.getElementById('displayed-phone');
            
            // Afficher le numéro de téléphone saisi
            if (phoneNumberInput && phoneNumberInput.value) {
                displayedPhone.textContent = '+224 ' + phoneNumberInput.value;
            }
            
            const orangeMoneyModal = new bootstrap.Modal(document.getElementById('orangeMoneyModal'));
            orangeMoneyModal.show();
        });
    }
    
    // Paycard Button Handler
    const paycardButton = document.getElementById('paycard-button');
    if (paycardButton) {
        paycardButton.addEventListener('click', function() {
            const paycardNumberInput = document.getElementById('paycard_number');
            const displayedPaycard = document.getElementById('displayed-paycard');
            
            // Afficher le numéro de Paycard saisi
            if (paycardNumberInput && paycardNumberInput.value) {
                displayedPaycard.textContent = paycardNumberInput.value;
            }
            
            const paycardModal = new bootstrap.Modal(document.getElementById('paycardModal'));
            paycardModal.show();
        });
    }
    
    // Gestionnaire pour le bouton "Renvoyer le code" Orange Money
    const resendCodeButton = document.getElementById('resend-code');
    if (resendCodeButton) {
        resendCodeButton.addEventListener('click', function() {
            alert('Un nouveau code a été envoyé à votre numéro.');
        });
    }
    
    // Gestionnaires de confirmation de paiement
    const confirmPaypal = document.getElementById('confirm-paypal');
    const confirmOrangeMoney = document.getElementById('confirm-orange-money');
    const confirmPaycard = document.getElementById('confirm-paycard');
    const checkoutForm = document.getElementById('checkout-form');
    
    function handlePaymentSuccess(paymentType, transactionId) {
        // Générer un numéro de commande aléatoire
        const orderNumber = 'ORD-' + Math.floor(100000 + Math.random() * 900000);
        document.getElementById('order-number').textContent = orderNumber;
        
        // Fermer tous les modaux
        const modals = ['paypalModal', 'orangeMoneyModal', 'paycardModal'];
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(document.getElementById(modal));
            if (modalInstance) {
                modalInstance.hide();
            }
        });
        
        // Définir la valeur du champ hidden correspondant au type de paiement
        if (paymentType === 'paypal') {
            document.getElementById('paypal_payment_id').value = transactionId;
        } else if (paymentType === 'orange-money') {
            document.getElementById('orange_money_transaction_id').value = transactionId;
        } else if (paymentType === 'paycard') {
            document.getElementById('paycard_transaction_id').value = transactionId;
        }
        
        // Afficher le modal de succès
        const successModal = new bootstrap.Modal(document.getElementById('paymentSuccessModal'));
        successModal.show();
        
        // Soumettre le formulaire après 5 secondes (simulation du traitement)
        setTimeout(function() {
            checkoutForm.submit();
        }, 5000);
    }
    
    if (confirmPaypal) {
        confirmPaypal.addEventListener('click', function() {
            const email = document.getElementById('paypal-email').value;
            const password = document.getElementById('paypal-password').value;
            
            if (!email || !password) {
                alert('Veuillez remplir tous les champs pour continuer.');
                return;
            }
            
            // Simuler une transaction PayPal réussie
            handlePaymentSuccess('paypal', 'PP-' + Date.now());
        });
    }
    
    if (confirmOrangeMoney) {
        confirmOrangeMoney.addEventListener('click', function() {
            const otpCode = document.getElementById('otp-code').value;
            
            if (!otpCode) {
                alert('Veuillez entrer le code d\'autorisation reçu par SMS.');
                return;
            }
            
            // Simuler une transaction Orange Money réussie
            handlePaymentSuccess('orange-money', 'OM-' + Date.now());
        });
    }
    
    if (confirmPaycard) {
        confirmPaycard.addEventListener('click', function() {
            const pin = document.getElementById('paycard-confirm-pin').value;
            
            if (!pin) {
                alert('Veuillez entrer votre code PIN pour confirmer le paiement.');
                return;
            }
            
            // Simuler une transaction Paycard réussie
            handlePaymentSuccess('paycard', 'PC-' + Date.now());
        });
    }
    
    // Validation du formulaire de carte bancaire
    const cardPaymentForm = document.querySelector('button[type="submit"]');
    if (cardPaymentForm) {
        cardPaymentForm.addEventListener('click', function(e) {
            // Si la méthode de paiement par carte est sélectionnée
            if (document.getElementById('card').checked) {
                const cardNumber = document.getElementById('card_number').value;
                const expiry = document.getElementById('expiry').value;
                const cvv = document.getElementById('cvv').value;
                const shippingAddress = document.getElementById(document.querySelector('textarea[name$="shipping_address"]').id).value;
                
                if (!cardNumber || !expiry || !cvv || !shippingAddress) {
                    e.preventDefault();
                    alert('Veuillez remplir tous les champs obligatoires.');
                    return;
                }
                
                // Vérifications simples de format
                if (!/^\d{16}$/.test(cardNumber.replace(/\s/g, ''))) {
                    e.preventDefault();
                    alert('Le format du numéro de carte est invalide.');
                    return;
                }
                
                if (!/^\d{2}\/\d{2}$/.test(expiry)) {
                    e.preventDefault();
                    alert('Le format de la date d\'expiration est invalide (MM/AA).');
                    return;
                }
                
                if (!/^\d{3}$/.test(cvv)) {
                    e.preventDefault();
                    alert('Le format du code CVV est invalide.');
                    return;
                }
                
                // Simuler une transaction par carte réussie
                e.preventDefault();
                handlePaymentSuccess('card', 'CB-' + Date.now());
            }
        });
    }
    
    // Formatage du numéro de carte en temps réel
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 16) {
                value = value.slice(0, 16);
            }
            // Formatage avec espaces tous les 4 chiffres
            let formattedValue = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += ' ';
                }
                formattedValue += value[i];
            }
            e.target.value = formattedValue;
        });
    }
    
    // Formatage de la date d'expiration en temps réel
    const expiryInput = document.getElementById('expiry');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 4) {
                value = value.slice(0, 4);
            }
            // Format MM/YY
            if (value.length > 2) {
                e.target.value = value.slice(0, 2) + '/' + value.slice(2);
            } else {
                e.target.value = value;
            }
        });
    }
    
    // Formatage du CVV en temps réel
    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 3) {
                value = value.slice(0, 3);
            }
            e.target.value = value;
        });
    }
});


