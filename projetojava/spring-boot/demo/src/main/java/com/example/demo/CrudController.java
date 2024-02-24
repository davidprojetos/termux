package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.List;

//...

@Controller
@RequestMapping("/crud")
public class CrudController {

    @Autowired
    private CrudService crudService;

    @GetMapping("/listar")
    public String listarRegistros(Model model) {
        List<Registro> registros = crudService.listarRegistros();
        model.addAttribute("registros", registros);
        return "listar";
    }

    @GetMapping("/form")
    public String exibirFormulario(Model model) {
        model.addAttribute("registro", new Registro());
        return "formulario";
    }

    @PostMapping("/salvar")
    public String salvarRegistro(@ModelAttribute Registro registro) {
        crudService.salvarRegistro(registro);
        return "redirect:/crud/listar";
    }

    @GetMapping("/editar/{id}")
    public String editarRegistro(@PathVariable Long id, Model model) {
        Registro registro = crudService.buscarRegistro(id);
        model.addAttribute("registro", registro);
        return "formulario";
    }

    @GetMapping("/excluir/{id}")
    public String excluirRegistro(@PathVariable Long id) {
        crudService.excluirRegistro(id);
        return "redirect:/crud/listar";
    }
}
