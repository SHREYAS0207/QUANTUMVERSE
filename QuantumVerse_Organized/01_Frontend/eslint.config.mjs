import nextVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

const config = [
	...nextVitals,
	...nextTypescript,
	{
		rules: {
			"@typescript-eslint/no-explicit-any": "warn",
			"@typescript-eslint/no-unused-vars": "warn",
			"react-hooks/purity": "warn",
			"react-hooks/set-state-in-effect": "warn",
			"react-hooks/static-components": "warn",
			"react/no-unescaped-entities": "warn",
			"@next/next/no-html-link-for-pages": "warn",
		},
	},
];

export default config;
