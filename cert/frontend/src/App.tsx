import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import logo from './assets/logo.svg';
import Footer from './components/common/Footer';
import ExportCertificateForm from './modules/Home';

const App: React.FC = () => {
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