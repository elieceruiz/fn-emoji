import React, { useEffect } from "react";

export default function MyKeyListener() {
  useEffect(() => {
    const handler = (e) => {
      window.parent.postMessage({ key: e.key }, "*");
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return <div>Key Listener Component Ready</div>;
}
