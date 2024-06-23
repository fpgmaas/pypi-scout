// app/components/GoogleAnalytics.tsx
"use client";

import { useEffect } from "react";

const GoogleAnalytics = () => {
  useEffect(() => {
    const trackingId = process.env.NEXT_PUBLIC_GA_TRACKING_ID;
    if (trackingId) {
      const script1 = document.createElement("script");
      script1.async = true;
      script1.src = `https://www.googletagmanager.com/gtag/js?id=${trackingId}`;
      document.head.appendChild(script1);

      const script2 = document.createElement("script");
      script2.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '${trackingId}');
      `;
      document.head.appendChild(script2);
    }
  }, []);

  return null;
};

export default GoogleAnalytics;
