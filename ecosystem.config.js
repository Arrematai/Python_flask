module.exports = {
	apps: [
		{
			name: "Arrematai",
			script: "poetry run arrematei",
			autorestart: true,
			watch: true,
			max_memory_restart: "250M",
			interpreter: "python",
		},
	],
};
