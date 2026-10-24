using System.Collections.Generic;

// Optional companion to the ModernTech data mod: every employee's skills are doubled once,
// up to the game's skill cap (100%), when they join your company or when you first load a game
// with this mod. Who has been doubled is kept in the save, so loading never doubles anyone twice.
public class ModernTechSkills : ModBehaviour
{
	public const float Factor = 2f;

	private const string SaveKey = "DoubledSkills";

	// Employee DIDs whose skills were already doubled; null until known for the current game
	private HashSet<uint> _doubled;

	private GameSettings _game;

	private float _readyAt;

	public override void OnActivate()
	{
	}

	public override void OnDeactivate()
	{
	}

	private void Update()
	{
		GameSettings gs = GameSettings.Instance;
		if (gs != _game)
		{
			// A new or loaded game: give loading a moment, then read who was already doubled
			_game = gs;
			_doubled = null;
			_readyAt = UnityEngine.Time.unscaledTime + 2f;
		}
		if (gs == null || gs.sActorManager == null || UnityEngine.Time.unscaledTime < _readyAt)
		{
			return;
		}
		if (_doubled == null)
		{
			_doubled = Parse(SavedValue(gs));
		}
		foreach (Actor actor in gs.sActorManager.Actors)
		{
			if (actor != null && actor.AItype == AI.AIType.Employee && actor.employee != null && _doubled.Add(actor.DID))
			{
				for (int i = 0; i < 5; i++)
				{
					Employee.EmployeeRole role = (Employee.EmployeeRole)i;
					actor.employee.ChangeSkillDirect(role, actor.employee.GetSkill(role) * Factor);
				}
			}
		}
	}

	public override void Serialize(WriteDictionary data, GameReader.LoadMode mode)
	{
		if (_doubled != null && _game == GameSettings.Instance)
		{
			data[SaveKey] = Join(_doubled);
		}
	}

	private string SavedValue(GameSettings gs)
	{
		WriteDictionary mine = gs.ModData == null || ParentMod == null ? null : gs.ModData.Get<WriteDictionary>(ParentMod.Meta.Name, null);
		return mine == null ? null : mine.Get<string>(SaveKey, null);
	}

	public static HashSet<uint> Parse(string saved)
	{
		HashSet<uint> ids = new HashSet<uint>();
		if (!string.IsNullOrEmpty(saved))
		{
			foreach (string part in saved.Split(','))
			{
				uint id;
				if (uint.TryParse(part, out id))
				{
					ids.Add(id);
				}
			}
		}
		return ids;
	}

	public static string Join(IEnumerable<uint> ids)
	{
		List<string> parts = new List<string>();
		foreach (uint id in ids)
		{
			parts.Add(id.ToString());
		}
		return string.Join(",", parts.ToArray());
	}
}
