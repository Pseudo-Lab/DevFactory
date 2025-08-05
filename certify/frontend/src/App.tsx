import React from 'react';
import Header from './components/common/Header';
import Hero from './modules/Home/components/Hero';
import Homepage from './modules/Home/index';
import Features from './modules/Home/components/Features';
import Footer from './components/common/Footer';
import logo from './assets/logo.png';

const App: React.FC = () => {
  return (
    <>
      <Header logoSrc={logo}/>
      <Hero />
      <Homepage />
      <Features />
      <Footer />
    </>
  );
};

export default App;