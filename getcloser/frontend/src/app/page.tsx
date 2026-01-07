'use client';

import Page1 from './pages/Page1';
import Page2 from './pages/Page2';
import Page3 from './pages/Page3';
import Page4 from './pages/Page4';
import { useNavigationStore } from '../store/navigationStore';

export default function Home() {
  const { currentPage } = useNavigationStore();

  const renderPage = () => {
    switch (currentPage) {
      case 'page1':
        return <Page1 />;
      case 'page2':
        return <Page2 />;
      case 'page3':
        return <Page3 />;
      case 'page4':
        return <Page4 />;
      default:
        return <Page1 />;
    }
  };

  return (
    <main className="flex flex-1 flex-col w-full h-full">
      {renderPage()}
    </main>
  );
}