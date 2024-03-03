// InteractiveButton.tsx
import React from 'react';

export default function InteractiveButton() {
    return (
        <button onClick={() => window.open('/showcase/demo1-fast-circle', '_blank')}>
            Open Demo 1
        </button>
    );
}
