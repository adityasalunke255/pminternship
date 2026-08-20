import React, { useEffect, useRef } from 'react';

const Header = () => {
  const hasInitialized = useRef(false);

  // Initialize Google Translate widget
  useEffect(() => {
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    const addGoogleTranslateScript = () => {
      if (!document.getElementById('google-translate-script')) {
        const script = document.createElement('script');
        script.id = 'google-translate-script';
        script.type = 'text/javascript';
        script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.body.appendChild(script);
        
        window.googleTranslateElementInit = () => {
          if (!window.google?.translate?.TranslateElement) return;
          new window.google.translate.TranslateElement(
            { pageLanguage: 'en', layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE },
            'google_translate_element'
          );
        };
      }
    };
    addGoogleTranslateScript();
  }, []);

  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <img 
            src="/pm_internship_logo_eng.svg" 
            alt="PM Internship Logo" 
            className="header-logo"
            style={{ height: '40px' }}
          />
          <img 
            src="/download.svg" 
            alt="Govt of India Logo" 
            className="header-logo"
            style={{ height: '40px' }}
          />
          <span className="header-title" style={{ fontSize: '1rem', fontWeight: 600 }}>PM Internship Scheme</span>
          <img 
            src="https://i.imgur.com/G5g25g3.png" 
            alt="AI Finder Logo" 
            className="header-logo"
            style={{ height: '40px' }}
          />
          <span className="header-title" style={{ fontSize: '1rem', fontWeight: 600 }}>AI-Based PM Internship Finder</span>
        </div>
        
        <nav className="header-nav">
          <a href="#">Home</a>
          <a href="https://pminternship.mca.gov.in/mca-api/files/get-file-by-path?path=U7k3z9vkJ6yFXfPI%2B4IVSnRblplXd0gMWwC7NmtDz3KvID8OvSm5GlAvf3kWvu8ZUpW3UeOTZFPrNIBREASgbtrFpqIz7BnLJtCXCyGMggExnO0bzUc3TuZU3GtUxLggfEZn4%2Bw4Xkl%2FgEYJJg%3D%3D">Guidelines</a>
          <a href="https://pminternship.mca.gov.in/login/#eligibility-criteria">Eligibility</a>
          <div id="google_translate_element" style={{ margin: '0 10px', minWidth: '150px' }}></div>
          <a href="https://pminternship.mca.gov.in/login/" className="header-login-btn">Login</a>
        </nav>
      </div>
    </header>
  );
};

export default Header;
