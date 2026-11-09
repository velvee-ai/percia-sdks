import { Command } from "commander";
import type { Context } from "../context.js";
import { CliError, EXIT } from "../errors.js";

type Node = { name: string; options: string[]; children: Node[] };
const walk = (c: Command): Node => ({ name: c.name(), options: c.options.flatMap((o) => [o.long, o.short].filter(Boolean) as string[]), children: c.commands.filter((x) => !(x as any)._hidden).map(walk) });

export function completionScript(shell: string, root: Command): string {
	const tree = walk(root);
	const bin = tree.name;
	const top = tree.children.map((c) => c.name);
	if (shell === "bash") {
		const cases = tree.children.filter((c) => c.children.length).map((c) => `    ${c.name}) COMPREPLY=( $(compgen -W "${c.children.map((x) => x.name).join(" ")} ${c.options.join(" ")}" -- "$cur") ) ; return ;;`).join("\n");
		return `# ${bin} bash completion: source <(${bin} completion bash)
_${bin}() {
  local cur="\${COMP_WORDS[COMP_CWORD]}"
  if [ "$COMP_CWORD" -eq 1 ]; then
    COMPREPLY=( $(compgen -W "${top.join(" ")} ${tree.options.join(" ")}" -- "$cur") ); return
  fi
  case "\${COMP_WORDS[1]}" in
${cases}
  esac
  COMPREPLY=( $(compgen -W "${tree.options.join(" ")}" -- "$cur") )
}
complete -F _${bin} ${bin}
`;
	}
	if (shell === "zsh") {
		const cases = tree.children.filter((c) => c.children.length).map((c) => `      ${c.name}) _values 'subcommand' ${c.children.map((x) => `'${x.name}'`).join(" ")} ;;`).join("\n");
		return `#compdef ${bin}
# ${bin} zsh completion: ${bin} completion zsh > "\${fpath[1]}/_${bin}"
_${bin}() {
  if (( CURRENT == 2 )); then
    _values 'command' ${top.map((x) => `'${x}'`).join(" ")}
    return
  fi
  case "$words[2]" in
${cases}
  esac
}
_${bin} "$@"
`;
	}
	if (shell === "fish") {
		const lines = [`# ${bin} fish completion: ${bin} completion fish > ~/.config/fish/completions/${bin}.fish`];
		for (const c of tree.children) {
			lines.push(`complete -c ${bin} -n '__fish_use_subcommand' -a ${c.name}`);
			for (const s of c.children) lines.push(`complete -c ${bin} -n '__fish_seen_subcommand_from ${c.name}' -a ${s.name}`);
		}
		return lines.join("\n") + "\n";
	}
	throw new CliError(`Unknown shell "${shell}".`, EXIT.USAGE, "Use bash, zsh or fish.");
}

export function registerCompletion(program: Command, ctx: Context) {
	program
		.command("completion <shell>")
		.description("Print a shell completion script (bash, zsh, fish).")
		.action((shell: string) => ctx.stdout(completionScript(shell, program)));
}
