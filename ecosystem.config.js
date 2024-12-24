module.exports = {
	apps: [
		{
			name: "Arrematai",
			script: "src/__main__.py",
			autorestart: true,
			watch: true,
			max_memory_restart: "250M",
			interpreter: "python",
		},
	],
};
