package ai.giskard.web.dto.ml;

import com.dataiku.j2ts.annotations.UIModel;
import com.dataiku.j2ts.annotations.UINullable;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotNull;

@Getter
@Setter
@NoArgsConstructor
@UIModel
public class ProjectPostDTO {
    @NotNull
    @UINullable
    private Long id;

    @NotNull
    private String name;

    @NotNull
    @UINullable
    private String key;
    @NotNull
    private String description;
}
