import React from "react";
import Image from "next/image";

export const CMIcons = {
  close: "/close.svg",
  burger: "/burger.svg",
  home: "/home.svg",
  knowledge: "/knowledge-icon.svg",
  profile: "/profile.svg",
  showCase: "/show-case.svg",
};

interface CMIconProps {
  iconName: keyof typeof CMIcons;
  width?: number;
  height?: number;
  edgeLength?: number;
  className?: string;
}

export default function CMIcon({
  iconName,
  width,
  height,
  edgeLength = 24,
  className,
  ...rest
}: CMIconProps) {
  return (
    <div
      style={{
        height: height ?? edgeLength,
        width: width ?? edgeLength,
        minHeight: height ?? edgeLength,
        minWidth: width ?? edgeLength,
      }}
      className={className}
    >
      <Image
        className={"w-full h-full object-contain"}
        src={CMIcons[iconName]}
        alt={iconName}
        height={height ?? edgeLength}
        width={width ?? edgeLength}
        {...rest}
      />
    </div>
  );
}
