import { ReactNode } from 'react';

import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

interface LayoutProps {
  children: ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-bg-primary text-primary">
      <TopBar />

      <div className="mx-auto flex max-w-[1600px] items-start pt-14">
        <Sidebar />

        <main className="min-w-0 flex-1 px-4 py-6 pb-24 lg:px-8 lg:py-8 lg:pb-10">{children}</main>
      </div>
    </div>
  );
};
