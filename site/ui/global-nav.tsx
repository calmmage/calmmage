'use client';

import {type Item, sections} from '@/lib/sections';
import Link from 'next/link';
import {useSelectedLayoutSegment} from 'next/navigation';
import {MenuAlt2Icon, XIcon} from '@heroicons/react/solid';
import clsx from 'clsx';
import {useState} from 'react';
import Byline from './byline';

export function GlobalNav() {
    const [isOpen, setIsOpen] = useState(false);
    const onClose = () => setIsOpen(false);

    return (
        <div className="fixed top-0 z-10 flex w-full flex-col border-b border-gray-800 bg-black lg:bottom-0 lg:z-auto lg:w-72 lg:border-b-0 lg:border-r lg:border-gray-800">
            <div className="flex h-14 items-center px-4 py-4 lg:h-auto">
                <Link
                    href="/"
                    className="group flex w-full items-center gap-x-2.5"
                    onClick={onClose}
                >
                    <h3 className="font-semibold tracking-wide text-gray-400 group-hover:text-gray-50">
                        App Router
                    </h3>
                </Link>
            </div>
            <button
                type="button"
                className="group absolute right-0 top-0 flex h-14 items-center gap-x-2 px-4 lg:hidden"
                onClick={() => setIsOpen(!isOpen)}
            >
                <div className="font-medium text-gray-100 group-hover:text-gray-400">
                    Menu
                </div>
                {isOpen ? (
                    <XIcon className="block w-6 text-gray-400" />
                ) : (
                    <MenuAlt2Icon className="block w-6 text-gray-400" />
                )}
            </button>

            <div
                className={clsx('overflow-y-auto lg:static lg:block', {
                    'fixed inset-x-0 bottom-0 top-14 mt-px bg-black': isOpen,
                    hidden: !isOpen,
                })}
            >
                <nav className="space-y-6 px-2 pb-24 pt-5">
                    {sections.map((section) => {
                        return (
                            <div key={section.name}>
                                <div className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-gray-400/80">
                                    <div>{section.name}</div>
                                </div>

                                <div className="space-y-1">
                                    {section.items.map((item) => (
                                        <GlobalNavItem key={item.slug} item={item} onClose={onClose} />
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </nav>
                <Byline className="absolute hidden sm:block" />
            </div>
        </div>
    );
}

export function GlobalNavItem({
    item,
    onClose,
}: {
    item: Item;
    onClose: () => false | void;
}) {
    const segment = useSelectedLayoutSegment();
    const isActive = item.slug === segment;

    return (
        <Link
            onClick={onClose}
            href={`/${item.slug}`}
            className={clsx(
                'block rounded-md px-3 py-2 text-sm font-medium hover:text-gray-300',
                {
                    'text-gray-400 hover:bg-gray-800': !isActive,
                    'text-white': isActive,
                },
            )}
        >
            {item.name}
        </Link>
    );
}
