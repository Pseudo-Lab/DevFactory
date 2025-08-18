import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import Hero from './modules/Home/components/Hero';
import Homepage from './modules/Home/index';
import Features from './modules/Home/components/Features';
import Footer from './components/common/Footer';
import logo from './assets/logo.png';
import ExportCertificateForm from './modules/NewHome/ExportCertificateForm';

const App: React.FC = () => {
  return (
    <>
      <Header logoSrc={logo}/>
      <Routes>
        <Route path="/" element={
          <>
            <Hero />
            <Homepage />
            <Features />
          </>
        } />
        <Route path="/new" element={<ExportCertificateForm />} />
      </Routes>
      <Footer />
    </>
  );
};

export default App;