import React, { useEffect, useRef } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/common/Header';
import logo from './assets/logo.svg';
import Footer from './components/common/Footer';
import ExportCertificateForm from './modules/Home';

const App: React.FC = () => {
  const location = useLocation();
  const lastPathRef = useRef<string | null>(null);

  useEffect(() => {
    const path = `${location.pathname}${location.search}${location.hash}`;
    if (lastPathRef.current === path) {
      return;
    }
    lastPathRef.current = path;

    fetch('/api/log/pageview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path }),
    }).catch(() => {
      // Logging failures should not affect user flow.
    });
  }, [location.pathname, location.search, location.hash]);

  return (
    <>
      <Header logoSrc={logo}/>
      <Routes>
        <Route path="/" element={
          <>
            <ExportCertificateForm />
          </>
        } />
      </Routes>
      <Footer />
    </>
  );
};

export default App;
